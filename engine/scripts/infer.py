#!/usr/bin/env python3
"""
Tradyxa RubiX - Daily Inference Script
Runs every 30 min (M-F 9:15 AM - 3:30 PM IST) via GitHub Actions

Loads pre-trained models, fetches live data, generates predictions.
Output: rubix_vault.json for dashboard consumption.

Implements:
- Fix #2: Model confidence tracking
- Fix #11: Weighted Traffic Light scoring (0-100)
- Fix #12: FOMO Meter with volume confirmation
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from data_fetcher import fetch_inference_data, get_live_price, fetch_global_sentiment
from feature_builder import build_features
from hmm_regime import infer_regime, MODELS_DIR
from rf_reversal import infer_reversal
from xgb_momentum import infer_momentum
from qr_range import infer_range
from gbm_divergence import infer_divergence
from probability_models import monte_carlo_cones, prob_touch_barrier, calculate_probability_surface
from risk_calculator import (
    calculate_var_cvar, kelly_regime_adjusted, calculate_win_rate,
    calculate_hurst_exponent, get_risk_free_rate
)
from friday_fear import get_friday_fear

# Output path
OUTPUT_DIR = Path(__file__).parent.parent.parent / "public" / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def traffic_light_score(regime: str, regime_prob: float, vix: float, momentum: int) -> dict:
    """
    Calculate weighted Traffic Light score.
    
    Fix #11: Use weighted scoring (0-100) instead of binary GO/WAIT/STOP.
    
    Components:
    - Regime: 40 points max
    - VIX: 30 points max
    - Momentum: 30 points max
    """
    score = 0
    breakdown = {}
    
    # Regime contribution (40 points max)
    if regime == 'TRENDING':
        regime_score = 40 * regime_prob
    elif regime == 'MEAN_REVERTING':
        regime_score = 20 * regime_prob
    else:  # CHAOTIC
        regime_score = 0
    score += regime_score
    breakdown['regime'] = regime_score
    
    # VIX contribution (30 points max)
    if vix < 15:
        vix_score = 30
    elif vix < 20:
        vix_score = 15
    elif vix < 24:
        vix_score = 5
    else:
        vix_score = 0
    score += vix_score
    breakdown['vix'] = vix_score
    
    # Momentum contribution (30 points max)
    momentum_score = min(momentum * 0.3, 30)
    score += momentum_score
    breakdown['momentum'] = momentum_score
    
    # Convert to traffic light
    if score > 70:
        signal = 'GO'
        verdict = 'Conditions favorable for new entries'
    elif score > 40:
        signal = 'WAIT'
        verdict = 'Mixed signals - reduce size, be selective'
    else:
        signal = 'STOP'
        verdict = 'Choppy/dangerous - avoid new positions'
    
    return {
        'signal': signal,
        'score': round(score, 1),
        'breakdown': breakdown,
        'verdict': verdict
    }


def fomo_meter_with_volume(rsi: float, bb_position: float, volume_ratio: float) -> dict:
    """
    Calculate FOMO Meter with volume confirmation.
    
    Fix #12: Reduce FOMO signal strength if volume is low.
    High RSI + low volume = weak FOMO signal (false breakout risk).
    """
    # Base FOMO calculation
    if rsi > 75 or bb_position > 0.95:
        base_fomo = 80
        zone = 'EXTREME_GREED'
        verdict_base = "Extreme greed - risk of buying top"
    elif rsi > 65 or bb_position > 0.85:
        base_fomo = 65
        zone = 'HIGH_GREED'
        verdict_base = "High greed - be cautious"
    elif rsi < 25 or bb_position < 0.05:
        base_fomo = 20
        zone = 'EXTREME_FEAR'
        verdict_base = "Extreme fear - risk of selling bottom"
    elif rsi < 35 or bb_position < 0.15:
        base_fomo = 35
        zone = 'HIGH_FEAR'
        verdict_base = "High fear - potential oversold"
    else:
        base_fomo = 50
        zone = 'NEUTRAL'
        verdict_base = "Neutral - no extreme emotion"
    
    # Volume confirmation (Fix #12)
    volume_confirmed = volume_ratio >= 0.8
    if not volume_confirmed:
        # Reduce FOMO if volume doesn't confirm
        adjusted_fomo = base_fomo * 0.7  # 30% discount
        volume_note = " (weak volume - signal discounted)"
    else:
        adjusted_fomo = base_fomo
        volume_note = ""
    
    return {
        'value': round(adjusted_fomo, 0),
        'base_value': base_fomo,
        'zone': zone,
        'volume_confirmed': volume_confirmed,
        'volume_ratio': round(volume_ratio, 2),
        'verdict': verdict_base + volume_note
    }


def calculate_theta_decay(spot: float, vix: float) -> dict:
    """Simple theta decay estimation based on VIX."""
    # Higher VIX = higher IV = more theta decay
    theta_per_day = -0.1 * (vix / 15) * (spot / 100)  # Rough estimate
    
    return {
        'value': round(theta_per_day, 1),
        'unit': 'pts/day',
        'verdict': "Seller's advantage" if vix > 15 else "Buyer window"
    }


def generate_overall_verdict(
    traffic: dict,
    regime: dict,
    momentum: dict,
    fomo: dict,
    var_result: dict,
    vix: float,
    hurst: float,
    kelly: dict,
    index: str
) -> dict:
    """
    Generate overall ML-based verdict synthesizing all signals.
    SEBI compliant - educational analysis, not financial advice.
    """
    # Count bullish/bearish signals
    bullish_signals = 0
    bearish_signals = 0
    total_signals = 0
    
    # Traffic Light
    if traffic['signal'] == 'GO':
        bullish_signals += 2  # Higher weight
    elif traffic['signal'] == 'STOP':
        bearish_signals += 2
    total_signals += 2
    
    # Regime
    if regime.get('regime') == 'TRENDING':
        bullish_signals += 1
    elif regime.get('regime') == 'CHAOTIC':
        bearish_signals += 1
    total_signals += 1
    
    # Momentum
    if momentum['score'] > 55:
        bullish_signals += 1
    elif momentum['score'] < 45:
        bearish_signals += 1
    total_signals += 1
    
    # VIX
    if vix < 15:
        bullish_signals += 1
    elif vix > 20:
        bearish_signals += 1
    total_signals += 1
    
    # VaR
    if var_result['var_95'] > -0.02:
        bullish_signals += 1
    else:
        bearish_signals += 1
    total_signals += 1
    
    # FOMO
    if fomo['value'] < 40:
        bullish_signals += 1  # Fear = buying opportunity
    elif fomo['value'] > 60:
        bearish_signals += 1  # Greed = dangerous
    total_signals += 1
    
    # Calculate consensus
    bullish_pct = (bullish_signals / total_signals) * 100
    bearish_pct = (bearish_signals / total_signals) * 100
    
    # Determine overall stance
    if bullish_signals >= 5:
        stance = 'BULLISH'
        action = 'Conditions favor LONG positions'
        strategy = 'Buy on dips, sell OTM puts, ride momentum'
    elif bearish_signals >= 5:
        stance = 'BEARISH'
        action = 'Conditions favor SHORT positions or hedging'
        strategy = 'Sell rallies, buy puts, reduce exposure'
    elif bullish_signals > bearish_signals:
        stance = 'LEAN BULLISH'
        action = 'Slight bullish edge detected'
        strategy = 'Small longs, tight stops, book profits early'
    elif bearish_signals > bullish_signals:
        stance = 'LEAN BEARISH'
        action = 'Slight bearish edge detected'
        strategy = 'Stay light, hedge positions, wait for clarity'
    else:
        stance = 'NEUTRAL'
        action = 'No clear directional edge'
        strategy = 'Range trading, iron condors, wait for breakout'
    
    # Build detailed summary
    regime_text = regime.get('regime', 'UNKNOWN')
    traffic_text = traffic['signal']
    kelly_text = kelly['kelly_pct']
    
    summary = f"{index} shows {regime_text} regime with {traffic_text} signal. ML consensus: {bullish_signals} bullish vs {bearish_signals} bearish signals out of {total_signals} total."
    
    return {
        'stance': stance,
        'action': action,
        'strategy': strategy,
        'summary': summary,
        'bullishSignals': bullish_signals,
        'bearishSignals': bearish_signals,
        'totalSignals': total_signals,
        'bullishPct': round(bullish_pct, 1),
        'kellySize': kelly_text,
    }


def generate_forecast_verdict(
    momentum: dict,
    regime: dict,
    rsi: float,
    vix: float,
    stance: str,
    global_sentiment: dict
) -> dict:
    """Generate Tomorrow/Intraday/Swing forecast using Technicals + Global Cues."""
    
    # 1. Tomorrow's Outlook (Technicals + Globals)
    tech_bias = 'BULLISH' if stance in ['BULLISH', 'LEAN BULLISH'] else 'BEARISH' if stance in ['BEARISH', 'LEAN BEARISH'] else 'NEUTRAL'
    
    # Global Sentiment Check
    global_bias = global_sentiment['sentiment']
    g_change = global_sentiment['change_pct']
    
    # Fuse Technical + Global
    if global_bias == 'BEARISH' and tech_bias == 'BULLISH':
        tomorrow = f"Gap Down likely (Global Weakness {g_change}% overrides Technicals)."
    elif global_bias == 'BULLISH' and tech_bias == 'BEARISH':
        tomorrow = f"Gap Up likely (Global Strength {g_change}% overrides Technicals)."
    elif global_bias == 'BEARISH' and tech_bias == 'BEARISH':
        tomorrow = f"Strong Gap Down likely (Global Drag {g_change}% confirms)."
    elif global_bias == 'BULLISH' and tech_bias == 'BULLISH':
        tomorrow = f"Strong Gap Up likely (Global Push {g_change}% confirms)."
    elif tech_bias == 'BULLISH':
        tomorrow = "Gap Up or Bullish Continuation likely."
    elif tech_bias == 'BEARISH':
        tomorrow = "Gap Down or Selling Pressure likely."
    else:
        tomorrow = "Flat/Range-bound expected."
    
    # Logic for Intraday 
    if vix > 18 or regime.get('regime') == 'CHAOTIC':
        intraday = "Scalp quickly. Don't hold losing trades."
    elif regime.get('regime') == 'TRENDING':
        intraday = "Trend Day likely. Buy pullbacks."
    else:
        intraday = "Range trading. Buy support, Sell resistance."

    # Logic for Swing
    if stance in ['BULLISH', 'LEAN BULLISH']:
        swing = "Hold BULLISH positions. Raise trailing stops."
    elif stance in ['BEARISH', 'LEAN BEARISH']:
        swing = "Hold BEARISH positions. Or stay Cash."
    else:
        swing = "Avoid overnight positions. Close EOD."

    return {
        'tomorrow': tomorrow,
        'intraday': intraday,
        'swing': swing
    }


def run_inference(index: str = 'NIFTY') -> dict:
    """
    Run full inference pipeline for dashboard.
    
    Args:
        index: 'NIFTY' or 'BANKNIFTY'
    
    Returns:
        Complete JSON structure for dashboard
    """
    print(f"Running inference for {index}...")
    
    # Fetch Global Sentiment (S&P Futures) for validation
    global_sentiment = fetch_global_sentiment()

    # Symbol mapping
    symbol = "^NSEI" if index == 'NIFTY' else "^NSEBANK"
    vix_symbol = "^INDIAVIX"
    
    # Fetch data
    print("  Fetching data...")
    index_df, vix_df, live_price = fetch_inference_data(index)  # Pass index to get NIFTY or BANKNIFTY
    if live_price == 0:
        live_price = float(index_df['Close'].iloc[-1])
    
    live_vix = get_live_price(vix_symbol)
    if live_vix == 0:
        live_vix = float(vix_df['Close'].iloc[-1])
    
    print(f"  Live price: {live_price}")
    print(f"  Live VIX: {live_vix}")
    
    # Build features
    print("  Building features...")
    features = build_features(index_df, vix_df)
    
    # Debug info
    print(f"  Features shape: {features.shape}")
    
    if len(features) == 0:
        print("  WARNING: Empty features after building. Using fallback values.")
        # Create minimal fallback
        latest = {
            'rsi_14': 50.0,
            'bb_position': 0.5,
            'volume_ratio': 1.0,
            'vix_5d_avg': live_vix,
            'vix_20d_avg': live_vix,
            'streak': 0,
        }
        features_empty = True
    else:
        latest = features.iloc[-1]
        features_empty = False
    
    # Run ML models
    print("  Running ML predictions...")
    
    # 1. Regime
    try:
        regime = infer_regime(features)
    except Exception as e:
        print(f"    Regime error: {e}")
        regime = {'regime': 'UNKNOWN', 'probability': 0.5, 'all_probabilities': {}}
    
    # 2. Reversal
    try:
        reversal = infer_reversal(features)
    except Exception as e:
        print(f"    Reversal error: {e}")
        reversal = {'adjusted_probability': 0.5, 'current_streak': 0, 'confidence': 'UNKNOWN'}
    
    # 3. Momentum
    try:
        momentum = infer_momentum(features)
    except Exception as e:
        print(f"    Momentum error: {e}")
        momentum = {'score': 50, 'strength': 'MEDIUM', 'verdict': 'Error'}
    
    # 4. Range
    try:
        range_pred = infer_range(features)
    except Exception as e:
        print(f"    Range error: {e}")
        range_pred = {'range_points': {'q50': 100}, 'expected_range': '±100 pts'}
    
    # 5. Divergence
    try:
        divergence = infer_divergence(features)
    except Exception as e:
        print(f"    Divergence error: {e}")
        divergence = {'detected': False, 'type': 'NONE', 'verdict': 'Error'}
    
    # Run statistical calculations
    print("  Running statistical calculations...")
    
    returns = index_df['Close'].pct_change().dropna()
    
    # VaR/CVaR
    var_result = calculate_var_cvar(returns)
    
    # Win rate and Kelly
    win_stats = calculate_win_rate(returns)
    kelly = kelly_regime_adjusted(
        win_stats['win_rate'],
        regime.get('regime', 'UNKNOWN'),
        win_stats['avg_win'],
        win_stats['avg_loss']
    )
    
    # Hurst cross-check
    hurst = calculate_hurst_exponent(index_df['Close'])
    if hurst > 0.6:
        hurst_verdict = "Strong Trend - Ride it"
    elif hurst < 0.4:
        hurst_verdict = "Choppy Market - Don't Chase"
    else:
        hurst_verdict = "Random Walk - No clear edge"
    
    # Friday Fear
    friday = get_friday_fear(index_df, live_price, global_sentiment=global_sentiment)
    
    # Dynamic Time-Aware Urgency (Friday Afternoon)
    now = datetime.now()
    if now.weekday() == 4: # Friday
        if 15 <= now.hour < 16:
            if now.minute < 30: # 3:00 PM - 3:29 PM
                friday['verdict'] = f"⚠ ACT NOW: {friday['verdict']}"
            else: # 3:30 PM - 3:59 PM
                friday['verdict'] = f"🔒 RISK LOCKED: {friday['verdict']}"
        elif now.hour >= 16:
             friday['verdict'] = f"🔒 MARKET CLOSED: {friday['verdict']}"
    
    # Monte Carlo
    mc = monte_carlo_cones(live_price, live_vix/100, T_days=5, returns=returns)
    
    # Barrier breach
    barrier_up = live_price * 1.02
    barrier_down = live_price * 0.98
    barrier_up_prob = prob_touch_barrier(live_price, barrier_up, live_vix/100, 5/252)
    barrier_down_prob = prob_touch_barrier(live_price, barrier_down, live_vix/100, 5/252)
    
    # Probability surface
    prob_surface = calculate_probability_surface(live_price, live_vix, returns)
    
    # VIX Term Structure
    vix_5d = float(features['vix_5d_avg'].iloc[-1])
    vix_20d = float(features['vix_20d_avg'].iloc[-1])
    # Contango: Spot < 5d < 20d (Healthy)
    # Backwardation: Spot > 5d (Fear)
    if live_vix > vix_5d:
        vix_term = 'Backwardation'
        term_verdict = "Fear rising - hedging active"
    elif vix_5d < vix_20d:
        vix_term = 'Contango'
        term_verdict = "Normal Market Structure"
    else:
        vix_term = 'Flat'
        term_verdict = "Uncertainty - wait"
    
    # Traffic Light (Fix #11)
    traffic = traffic_light_score(
        regime.get('regime', 'UNKNOWN'),
        regime.get('probability', 0.5),
        live_vix,
        momentum.get('score', 50)
    )

    # Conflict Resolution: Force Kelly to 0 if Traffic is STOP
    if traffic['signal'] == 'STOP':
        kelly['kelly_pct'] = "0%"
        kelly['kelly_fraction'] = 0.0
        kelly['verdict'] = "Cash is King (Traffic STOP)"
    
    # FOMO Meter (Fix #12)
    fomo = fomo_meter_with_volume(
        float(latest['rsi_14']),
        float(latest['bb_position']),
        float(latest['volume_ratio'])
    )
    
    # Theta
    theta = calculate_theta_decay(live_price, live_vix)
    
    # Daily change calculation
    prev_close = float(index_df['Close'].iloc[-2]) if len(index_df) > 1 else live_price
    daily_change = (live_price - prev_close) / prev_close
    
    # Pivot Points (S1) Support Calculation
    # Uses yesterday's data (row -2) since row -1 is active today
    if len(index_df) > 1:
        y_high = float(index_df['High'].iloc[-2])
        y_low = float(index_df['Low'].iloc[-2])
        y_close = float(index_df['Close'].iloc[-2])
        pivot_p = (y_high + y_low + y_close) / 3
        pivot_s1 = 2 * pivot_p - y_high
    else:
        pivot_s1 = live_price * 0.99 # Fallback
    
    # Calculate overall verdict and forecast
    overall_verdict = generate_overall_verdict(
        traffic=traffic,
        regime=regime,
        momentum=momentum,
        fomo=fomo,
        var_result=var_result,
        vix=live_vix,
        hurst=hurst,
        kelly=kelly,
        index=index
    )
    
    forecast = generate_forecast_verdict(
        momentum=momentum,
        regime=regime,
        rsi=float(latest['rsi_14']),
        vix=live_vix,
        stance=overall_verdict['stance'],
        global_sentiment=global_sentiment
    )
    
    # Time-Aware Context for Hero Header
    now = datetime.now()
    if 9 <= now.hour < 10 and now.minute < 15:
        time_context = "PRE-MARKET: "
    elif 9 <= now.hour < 10:
        time_context = "OPENING BELL: "
    elif 15 <= now.hour < 16 and now.minute < 30:
        time_context = "CLOSING HOUR: "
    elif now.hour >= 16 or now.hour < 9:
        time_context = "POST-MARKET: "
    else:
        time_context = "" # Mid-day standard

    # Build output JSON matching frontend types.ts
    output = {
        'generated_at': datetime.now().isoformat(),
        'indexName': index,
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        
        'hero': {
            'verdictTitle': f"{time_context}{overall_verdict['stance']} CONSENSUS",
            'verdictSubtitle': regime.get('regime', 'UNKNOWN') + f" regime with {regime.get('probability', 0)*100:.0f}% confidence",
            'bullishProbability': min(max(momentum['score'] + (10 if regime.get('regime') == 'TRENDING' else -10 if regime.get('regime') == 'CHAOTIC' else 0), 0), 100),
            'riskLevel': int(max(0, 100 - traffic['score'])),
            'riskVerdict': 'Low Risk' if traffic['score'] > 70 else 'Moderate Risk' if traffic['score'] > 40 else 'High Risk',
            'kellySize': int(kelly['kelly_fraction'] * 100),
            'kellyVerdict': kelly['verdict']
        },
        
        'tiles': {
            'spotPrice': {
                'id': 'spot',
                'label': 'Current Level',
                'value': int(live_price),
                'change': round(daily_change * 100, 2),
                'trend': 'up' if daily_change > 0 else 'down' if daily_change < 0 else 'neutral',
                'verdict': f"{'Above' if daily_change > 0 else 'Below'} prev close ({abs(daily_change)*100:.2f}%)"
            },
            
            'indiaVix': {
                'id': 'vix',
                'label': 'Fear Gauge (VIX)',
                'value': round(live_vix, 1),
                'change': round((live_vix - vix_5d) / vix_5d * 100, 1) if vix_5d > 0 else 0,
                'trend': 'up' if live_vix > vix_5d else 'down',
                'verdict': 'LOW VIX - Safe to trade options' if live_vix < 15 else 'ELEVATED VIX - Reduce position size' if live_vix < 20 else 'HIGH VIX - Avoid buying options'
            },
            
            'probabilitySurface': {
                'id': 'probs',
                'label': 'Option Skew',
                'value': prob_surface['skew'],
                'verdict': f"Calls: {prob_surface['call_bias']*100:.0f}%, Puts: {prob_surface['put_bias']*100:.0f}%",
                'meta': {'call': int(prob_surface['call_bias']*100), 'put': int(prob_surface['put_bias']*100)}
            },
            
            'regimeBeacon': {
                'id': 'regime',
                'label': 'Market Regime',
                'value': regime.get('regime', 'UNKNOWN'),
                'verdict': f"{'GO WITH TREND - momentum works' if regime.get('regime') == 'TRENDING' else 'BUY DIPS, SELL RALLIES - contrarian works' if regime.get('regime') == 'MEAN_REVERTING' else 'CHOPPY MARKET - stay out'}",
                'meta': {'type': regime.get('regime', 'unknown').lower(), 'all_probs': regime.get('all_probabilities', {})}
            },
            
            'kellyOptimal': {
                'id': 'kelly',
                'label': 'Bet Size',
                'value': kelly['kelly_pct'],
                'verdict': f"Use only {kelly['kelly_pct']} of your capital per trade"
            },
            
            'varGauge': {
                'id': 'var',
                'label': 'Max Daily Loss',
                'value': f"{var_result['var_95']*100:.1f}%",
                'verdict': 'NORMAL RISK - Proceed with trades' if var_result['var_95'] > -0.02 else 'HIGH RISK DAY - Go smaller'
            },
            
            'hurstCompass': {
                'id': 'hurst',
                'label': 'Trend Strength',
                'value': round(hurst, 2),
                'verdict': hurst_verdict
            },
            
            'vixTerm': {
                'id': 'vixterm',
                'label': 'Volatility Term',
                'value': vix_term,
                'verdict': term_verdict,
                'history': [
                    {'time': 'Spot', 'value': round(live_vix, 1)},
                    {'time': '5d Avg', 'value': round(vix_5d, 1)},
                    {'time': '20d Avg', 'value': round(vix_20d, 1)}
                ]
            },
            
            'fridayFear': {
                'id': 'fear',
                'label': 'Weekend Risk',
                'value': friday['risk_level'],
                'verdict': friday['verdict'][:50]  # Truncate
            },
            
            'thetaDecay': {
                'id': 'theta',
                'label': 'Time Decay',
                'value': theta['value'],
                'unit': theta['unit'],
                'verdict': 'Sellers Winning (Fast Decay)' if theta['value'] < -15 else 'Decay is Slow (Buyers Safe)'
            },
            
            'monteCarlo': {
                'id': 'mc',
                'label': 'Prediction (5d)',
                'value': 'Stable' if abs(mc['cones']['day_5']['median'] - live_price) < live_price * 0.01 else 'Volatile',
                'verdict': f"1σ: {mc['cones']['day_5']['1sigma_low']:.0f}-{mc['cones']['day_5']['1sigma_high']:.0f}"
            },
            
            'barrierBreach': {
                'id': 'barrier',
                'label': 'Touch Probability',
                'value': f"{max(barrier_up_prob, barrier_down_prob)*100:.0f}%",
                'verdict': f"±2% touch: Up {barrier_up_prob*100:.0f}%, Down {barrier_down_prob*100:.0f}%"
            },
            
            'streakReversal': {
                'id': 'streak',
                'label': 'Reversal Chance',
                'value': 'High' if reversal['adjusted_probability'] > 0.6 else 'Low' if reversal['adjusted_probability'] < 0.4 else 'Medium',
                'verdict': f"Streak: {reversal['current_streak']}d, P(rev): {reversal['adjusted_probability']*100:.0f}%"
            },
            
            'painZone': {
                'id': 'pain',
                'label': 'Expiry Pin',
                'value': round(live_price / 100) * 100,  # Round to nearest 100
                'verdict': f"MAGNET LEVEL - Price sticks near {round(live_price / 100) * 100}"
            },
            
            'rangeQuartiles': {
                'id': 'range',
                'label': 'Expected Range',
                'value': f"±{range_pred['range_points'].get('q50', 100):.0f}",
                'verdict': range_pred.get('expected_range', '±100 pts')
            },
            
            'momentumPulse': {
                'id': 'momentum',
                'label': 'Momentum',
                'value': f"+{momentum['score']}" if momentum['score'] > 50 else str(momentum['score']),
                'verdict': momentum.get('verdict', '')
            },
            
            'gexCluster': {
                'id': 'gex',
                'label': 'Key Support (S1)',
                'value': f"{int(pivot_s1)}",
                'verdict': f"Price floor at {int(pivot_s1)}"
            },
            
            'eventRadar': {
                'id': 'event',
                'label': 'Next Event',
                'value': 'Market Open' if (now.hour == 9 and now.minute < 15) else 
                         'Closing Bell' if (now.hour == 15 and now.minute < 30) else
                         'Weekly Expiry' if now.weekday() < 4 else 'Weekend',
                'verdict': f"Opening in {15-now.minute}m" if (now.hour == 9 and now.minute < 15) else
                           f"Closing in {30-now.minute}m" if (now.hour == 15 and now.minute < 30) else
                           f"{(4 - now.weekday())}d to expiry" if now.weekday() < 4 else 'Markets closed'
            },
            
            'trafficLight': {
                'id': 'traffic',
                'label': 'System Status',
                'value': traffic['signal'],
                'verdict': f"{'ALL CLEAR - Safe to trade' if traffic['signal'] == 'GO' else 'MIXED SIGNALS - Be selective' if traffic['signal'] == 'WAIT' else 'DANGER ZONE - Stay cash'}"
            },
            
            'fomoMeter': {
                'id': 'fomo',
                'label': 'Greed Meter',
                'value': int(fomo['value']),
                'verdict': f"{'EXTREME FEAR - Good time to buy' if fomo['value'] < 30 else 'NEUTRAL - No rush to trade' if fomo['value'] < 60 else 'EXTREME GREED - Avoid FOMO buying'}"
            }
        },
        
        # Overall Verdict - ML Summary for traders
        # Overall Verdict - ML Summary for traders
        'overallVerdict': overall_verdict,
        
        # Forecast for Tomorrow/Intraday/Swing
        'forecast': forecast
    }
    
    return output


def main():
    """Main inference function."""
    print("=" * 60)
    print("TRADYXA RUBIX - DAILY INFERENCE")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Run inference for both indices
    for index in ['NIFTY', 'BANKNIFTY']:
        print(f"\n{'='*40}")
        result = run_inference(index)
        
        # Save individual JSON file
        output_path = OUTPUT_DIR / f"rubix_{index.lower()}.json"
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"  ✅ {index} saved to: {output_path}")
        print(f"     Spot: {result['tiles']['spotPrice']['value']}")
        print(f"     Traffic: {result['tiles']['trafficLight']['value']}")
    
    # Also save NIFTY as the default rubix_vault.json for backward compat
    nifty_result = run_inference('NIFTY')
    with open(OUTPUT_DIR / "rubix_vault.json", 'w') as f:
        json.dump(nifty_result, f, indent=2)
    
    print(f"\n{'='*60}")
    print("✅ All indices processed!")


if __name__ == "__main__":
    main()
