#!/usr/bin/env python3
"""
Tradyxa RubiX - Friday Fear Index
Weekend gap risk analysis for F&O positions

=== Fix #10: Expiry Week vs Normal Week ===
Weekend gaps are larger during monthly expiry weeks.
We separate the analysis into expiry vs non-expiry weeks
for more accurate risk assessment.
"""

import numpy as np
import pandas as pd
from datetime import datetime


def is_expiry_week(date: datetime) -> bool:
    """
    Check if date falls in monthly expiry week (last Thursday of month).
    
    Args:
        date: Date to check
    
    Returns:
        True if date is in expiry week
    """
    # Get last Thursday of the month
    year = date.year
    month = date.month
    
    # Find last day of month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    
    last_day = (next_month - pd.Timedelta(days=1)).day
    
    # Find last Thursday (weekday 3)
    for day in range(last_day, last_day - 7, -1):
        try:
            check_date = datetime(year, month, day)
            if check_date.weekday() == 3:  # Thursday
                # Expiry week is the week containing this Thursday
                expiry_date = check_date
                week_start = expiry_date - pd.Timedelta(days=expiry_date.weekday())
                week_end = week_start + pd.Timedelta(days=6)
                
                return week_start.date() <= date.date() <= week_end.date()
        except:
            continue
    
    return False


def calculate_friday_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Friday-to-Monday gaps with expiry week flag.
    
    Args:
        df: DataFrame with OHLCV data
    
    Returns:
        DataFrame with gap information
    """
    df = df.copy()
    df['day_of_week'] = df.index.dayofweek
    
    # Get Fridays
    fridays = df[df['day_of_week'] == 4].copy()
    
    # Calculate gap to next trading day
    gaps = []
    for i, (idx, row) in enumerate(fridays.iterrows()):
        # Find next trading day (usually Monday)
        next_days = df[df.index > idx].head(3)
        if len(next_days) == 0:
            continue
        
        next_open = next_days['Open'].iloc[0]
        friday_close = row['Close']
        
        gap_pct = (next_open - friday_close) / friday_close
        
        gaps.append({
            'date': idx,
            'friday_close': friday_close,
            'monday_open': next_open,
            'gap_pct': gap_pct,
            'gap_abs': abs(gap_pct),
            'is_expiry': is_expiry_week(idx)
        })
    
    return pd.DataFrame(gaps)


def friday_fear_adjusted(df: pd.DataFrame, is_current_expiry: bool = None, global_sentiment: dict = None) -> dict:
    """
    Calculate Friday Fear Index with expiry week adjustment.
    
    Fix #10: Separate logic for expiry vs non-expiry weeks.
    
    Args:
        df: DataFrame with OHLCV data
        is_current_expiry: Whether current week is expiry week
        global_sentiment: Global market stance (e.g. {'sentiment': 'BEARISH'})
    
    Returns:
        Dict with gap statistics and risk assessment
    """
    # Calculate all gaps
    gaps_df = calculate_friday_gaps(df)
    
    if len(gaps_df) == 0:
        return {
            'risk_level': 'UNKNOWN',
            'gap_50': 0.0,
            'gap_75': 0.0,
            'gap_90': 0.0,
            'is_expiry_week': is_current_expiry,
            'verdict': 'Insufficient data'
        }
    
    # Split by expiry status
    expiry_gaps = gaps_df[gaps_df['is_expiry'] == True]['gap_abs']
    normal_gaps = gaps_df[gaps_df['is_expiry'] == False]['gap_abs']
    
    # Determine which group to use
    if is_current_expiry is None:
        is_current_expiry = is_expiry_week(datetime.now())
    
    if is_current_expiry and len(expiry_gaps) > 5:
        active_gaps = expiry_gaps
        week_type = 'EXPIRY'
    elif not is_current_expiry and len(normal_gaps) > 5:
        active_gaps = normal_gaps
        week_type = 'NORMAL'
    else:
        active_gaps = gaps_df['gap_abs']
        week_type = 'MIXED'
    
    # Calculate percentiles
    gap_50 = float(np.percentile(active_gaps, 50))
    gap_75 = float(np.percentile(active_gaps, 75))
    gap_90 = float(np.percentile(active_gaps, 90))
    
    # Determine risk level (Base)
    if gap_90 > 0.02:  # >2% gap at 90th percentile
        risk_level = 'HIGH'
        verdict = 'Significant gap risk - reduce overnight positions'
    elif gap_75 > 0.015:  # >1.5% at 75th percentile
        risk_level = 'MODERATE'
        verdict = 'Moderate gap risk - hedge weekend positions'
    else:
        risk_level = 'LOW'
        verdict = 'Low gap risk - weekend positions acceptable'
    
    # Global Adjustment logic
    global_note = ""
    if global_sentiment:
        g_sent = global_sentiment.get('sentiment', 'NEUTRAL')
        g_change = global_sentiment.get('change_pct', 0)
        
        if g_sent == 'BEARISH' and risk_level == 'LOW':
            risk_level = 'MODERATE'
            verdict = 'Global weakness detects carry risk.'
            global_note = f" (Global {g_change}%)"
        elif g_sent == 'BEARISH' and risk_level == 'MODERATE':
            risk_level = 'HIGH'
            verdict = 'Globally bearish. Do not hold longs.'
            global_note = f" (Global {g_change}%)"
            
    # Expiry adjustment
    if is_current_expiry:
        verdict = f"[EXPIRY WEEK] {verdict}"
        
    verdict += global_note
    
    return {
        'risk_level': risk_level,
        'gap_50': gap_50,
        'gap_75': gap_75,
        'gap_90': gap_90,
        'is_expiry_week': is_current_expiry,
        'week_type': week_type,
        'sample_size': len(active_gaps),
        'verdict': verdict,
        'gap_50_pts': None,  # Set by caller with spot price
        'gap_75_pts': None,
        'gap_90_pts': None
    }


def get_friday_fear(df: pd.DataFrame, spot_price: float, global_sentiment: dict = None) -> dict:
    """
    Get Friday Fear index with point values.
    
    Args:
        df: DataFrame with OHLCV data
        spot_price: Current spot price
        global_sentiment: Optional global market sentiment dict
    """
    result = friday_fear_adjusted(df, global_sentiment=global_sentiment)
    
    # Add point values
    result['gap_50_pts'] = result['gap_50'] * spot_price
    result['gap_75_pts'] = result['gap_75'] * spot_price
    result['gap_90_pts'] = result['gap_90'] * spot_price
    
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("TRADYXA RUBIX - FRIDAY FEAR TEST")
    print("=" * 60)
    
    # Test with sample data
    import yfinance as yf
    
    nifty = yf.download("^NSEI", period="5y", progress=False)
    
    # Check current expiry status
    today = datetime.now()
    print(f"\nCurrent date: {today.date()}")
    print(f"Is expiry week: {is_expiry_week(today)}")
    
    # Calculate Friday Fear
    spot = float(nifty['Close'].iloc[-1])
    result = get_friday_fear(nifty, spot)
    
    print(f"\nFriday Fear Analysis (Fix #10):")
    print(f"  Week type: {result['week_type']}")
    print(f"  Risk level: {result['risk_level']}")
    print(f"  Gap 50th percentile: {result['gap_50']:.2%} ({result['gap_50_pts']:.0f} pts)")
    print(f"  Gap 75th percentile: {result['gap_75']:.2%} ({result['gap_75_pts']:.0f} pts)")
    print(f"  Gap 90th percentile: {result['gap_90']:.2%} ({result['gap_90_pts']:.0f} pts)")
    print(f"  Verdict: {result['verdict']}")
