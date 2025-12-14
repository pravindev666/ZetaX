#!/usr/bin/env python3
"""
Tradyxa RubiX - Data Fetcher
Fetches NIFTY, BANKNIFTY, and India VIX data from yfinance
"""

import os
import time
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# Data directory
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def fetch_historical_data(symbol: str, start_date: str = "2005-01-01") -> pd.DataFrame:
    """
    Fetch full historical OHLCV data for a symbol.
    
    Args:
        symbol: Yahoo Finance ticker (e.g., "^NSEI")
        start_date: Start date for historical data
    
    Returns:
        DataFrame with OHLCV data
    """
    print(f"Fetching {symbol} from {start_date}...")
    
    df = yf.download(
        symbol,
        start=start_date,
        end=datetime.now().strftime("%Y-%m-%d"),
        progress=False,
        auto_adjust=True
    )
    
    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    print(f"  → {len(df)} rows ({df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')})")
    return df


def fetch_recent_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch recent data for inference.
    
    Args:
        symbol: Yahoo Finance ticker
        period: Period string (e.g., "1y", "6mo")
    
    Returns:
        DataFrame with OHLCV data
    """
    df = yf.download(symbol, period=period, progress=False, auto_adjust=True)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    return df


def get_live_price(symbol: str) -> float:
    """
    Get live/last traded price for a symbol.
    
    Args:
        symbol: Yahoo Finance ticker
    
    Returns:
        Current price as float
    """
    try:
        ticker = yf.Ticker(symbol)
        # Try fast_info first, fallback to history
        price = ticker.fast_info.get('lastPrice')
        if price is None:
            hist = ticker.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
        return float(price) if price else 0.0
    except Exception as e:
        print(f"Error fetching live price for {symbol}: {e}")
        return 0.0


def fetch_all_training_data() -> tuple:
    """
    Fetch all data needed for model training.
    Uses cached CSV if available and recent.
    
    Returns:
        Tuple of (nifty_df, banknifty_df, vix_df)
    """
    # File paths
    nifty_path = DATA_DIR / "NSEI_daily.csv"
    banknifty_path = DATA_DIR / "NSEBANK_daily.csv"
    vix_path = DATA_DIR / "INDIAVIX_daily.csv"
    
    # Fetch and save NIFTY
    nifty = fetch_historical_data("^NSEI", "2005-01-01")
    nifty.to_csv(nifty_path)
    time.sleep(2)  # Rate limit
    
    # Fetch and save BANKNIFTY
    banknifty = fetch_historical_data("^NSEBANK", "2005-01-01")
    banknifty.to_csv(banknifty_path)
    time.sleep(2)  # Rate limit
    
    # Fetch and save VIX (available from 2008)
    vix = fetch_historical_data("^INDIAVIX", "2008-01-01")
    vix.to_csv(vix_path)
    
    return nifty, banknifty, vix


def load_cached_data() -> tuple:
    """
    Load cached data from CSV files.
    
    Returns:
        Tuple of (nifty_df, banknifty_df, vix_df)
    """
    nifty = pd.read_csv(DATA_DIR / "NSEI_daily.csv", index_col=0, parse_dates=True)
    banknifty = pd.read_csv(DATA_DIR / "NSEBANK_daily.csv", index_col=0, parse_dates=True)
    vix = pd.read_csv(DATA_DIR / "INDIAVIX_daily.csv", index_col=0, parse_dates=True)
    
    return nifty, banknifty, vix


def fetch_inference_data(index: str = 'NIFTY') -> tuple:
    """
    Fetch data needed for daily inference (recent 1 year + live).
    
    Args:
        index: 'NIFTY' or 'BANKNIFTY'
    
    Returns:
        Tuple of (index_df, vix_df, live_price)
    """
    # Symbol mapping
    symbol = "^NSEI" if index == 'NIFTY' else "^NSEBANK"
    
    index_df = fetch_recent_data(symbol, "1y")
    time.sleep(2)  # Rate limit
    vix = fetch_recent_data("^INDIAVIX", "1y")
    time.sleep(2)  # Rate limit
    live_price = get_live_price(symbol)
    
    return index_df, vix, live_price


def fetch_global_sentiment() -> dict:
    """
    Fetch global market sentiment (S&P Futures).
    Used to validate 'Tomorrow's Outlook'.
    """
    try:
        # Fetch S&P 500 Futures (ES=F) - Proxy for Global/US Sentiment
        # Works 24/5, giving better overnight cues than Spot
        symbol = "ES=F"
        ticker = yf.Ticker(symbol)
        
        # Use fast_info for speed
        last_price = ticker.fast_info.last_price
        prev_close = ticker.fast_info.previous_close
        
        if last_price and prev_close:
            change_pct = ((last_price - prev_close) / prev_close) * 100
            sentiment = 'BULLISH' if change_pct > 0.25 else 'BEARISH' if change_pct < -0.25 else 'NEUTRAL'
            
            print(f"  Global Sentinel ({symbol}): {last_price:.2f} ({change_pct:+.2f}%) -> {sentiment}")
            
            return {
                'symbol': symbol,
                'change_pct': round(change_pct, 2),
                'sentiment': sentiment
            }
        
    except Exception as e:
        print(f"  ⚠️ Warning: Failed to fetch global sentiment: {e}")
    
    # Fallback
    return {'symbol': 'ES=F', 'change_pct': 0.0, 'sentiment': 'NEUTRAL'}


if __name__ == "__main__":
    print("=" * 60)
    print("TRADYXA RUBIX - DATA FETCHER")
    print("=" * 60)
    
    nifty, banknifty, vix = fetch_all_training_data()
    
    print("\n✅ Data saved to engine/data/")
    print(f"   NIFTY: {len(nifty)} rows")
    print(f"   BANKNIFTY: {len(banknifty)} rows")
    print(f"   VIX: {len(vix)} rows")
