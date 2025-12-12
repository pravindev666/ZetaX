#!/usr/bin/env python3
"""
Tradyxa RubiX - Risk Calculator
VaR, CVaR, Kelly Criterion, and model confidence calculations

=== Fix #2: Model Confidence Metric ===
Track rolling accuracy over last 5 days.
If accuracy drops below 55%, show warning that model may be stale.

=== Fix #4: Regime-Adjusted Kelly ===
Kelly formula adjusted based on current market regime:
- TRENDING: 10% boost (higher win rate expected)
- CHAOTIC: 20% reduction (lower win rate expected)
- MEAN_REVERTING: No adjustment

=== Fix #8: Dynamic Risk-Free Rate ===
Use India 10Y G-Sec yield (~7%) instead of hardcoded 5%.
"""

import numpy as np
import pandas as pd


def get_risk_free_rate() -> float:
    """
    Get current risk-free rate.
    
    Fix #8: Use India 10Y G-Sec yield as proxy (~7% as of Dec 2024).
    In production, this could fetch from RBI data.
    
    Returns:
        Risk-free rate as decimal (e.g., 0.07 for 7%)
    """
    # India 10Y G-Sec yield - update monthly
    return 0.07


def calculate_var_cvar(returns: pd.Series, confidence: float = 0.95) -> dict:
    """
    Calculate Value at Risk (VaR) and Conditional VaR (CVaR).
    
    BlackRock Aladdin-style tail risk quantification.
    
    Args:
        returns: Daily returns series
        confidence: Confidence level (0.95 or 0.99)
    
    Returns:
        Dict with VaR and CVaR values
    """
    returns = returns.dropna()
    
    # Historical VaR
    var_percentile = (1 - confidence) * 100
    var = float(np.percentile(returns, var_percentile))
    
    # CVaR (Expected Shortfall) - average of losses beyond VaR
    tail_losses = returns[returns <= var]
    cvar = float(tail_losses.mean()) if len(tail_losses) > 0 else var
    
    return {
        'var_95': float(np.percentile(returns, 5)),
        'var_99': float(np.percentile(returns, 1)),
        'cvar_95': cvar,
        'var_level': confidence,
        'sample_size': len(returns)
    }


def kelly_criterion_basic(win_rate: float, avg_win: float, avg_loss: float) -> float:
    """
    Basic Kelly Criterion calculation.
    
    f* = (p * b - q) / b
    where: p=win_rate, q=1-p, b=win/loss ratio
    
    Args:
        win_rate: Probability of winning (0-1)
        avg_win: Average winning trade return
        avg_loss: Average losing trade return (positive number)
    
    Returns:
        Kelly fraction (fraction of capital to bet)
    """
    if avg_loss == 0 or avg_win == 0:
        return 0.10  # Default conservative
    
    b = abs(avg_win / avg_loss)  # Win/loss ratio
    p = win_rate
    q = 1 - p
    
    f_star = (p * b - q) / b
    
    # Fractional Kelly (1/4) for conservatism
    return float(np.clip(f_star * 0.25, 0.05, 0.25))


def kelly_regime_adjusted(
    base_win_rate: float,
    current_regime: str,
    avg_win: float,
    avg_loss: float
) -> dict:
    """
    Regime-adjusted Kelly Criterion.
    
    Fix #4: Adjust Kelly based on current market regime.
    - TRENDING: Win rate boosted 10% (momentum strategies outperform)
    - CHAOTIC: Win rate reduced 20% (unpredictable outcomes)
    - MEAN_REVERTING: No adjustment
    
    Args:
        base_win_rate: Historical win rate
        current_regime: Current regime from HMM
        avg_win: Average winning trade return
        avg_loss: Average losing trade return
    
    Returns:
        Dict with Kelly sizing and adjustments
    """
    # Adjust win rate based on regime
    if current_regime == 'TRENDING':
        adjusted_win_rate = base_win_rate * 1.10  # 10% boost
        adjustment = 'BOOST'
        adjustment_pct = '+10%'
    elif current_regime == 'CHAOTIC':
        adjusted_win_rate = base_win_rate * 0.80  # 20% reduction
        adjustment = 'REDUCE'
        adjustment_pct = '-20%'
    else:  # MEAN_REVERTING or unknown
        adjusted_win_rate = base_win_rate
        adjustment = 'NONE'
        adjustment_pct = '0%'
    
    # Cap adjusted rate at 0.85
    adjusted_win_rate = min(adjusted_win_rate, 0.85)
    
    # Calculate Kelly
    if avg_loss == 0:
        kelly_pct = 0.10
    else:
        b = abs(avg_win / avg_loss)
        f_star = (adjusted_win_rate * b - (1 - adjusted_win_rate)) / b
        kelly_pct = float(np.clip(f_star * 0.25, 0.05, 0.25))
    
    return {
        'kelly_fraction': kelly_pct,
        'kelly_pct': f"{kelly_pct:.0%}",
        'base_win_rate': base_win_rate,
        'adjusted_win_rate': adjusted_win_rate,
        'regime': current_regime,
        'adjustment': adjustment,
        'adjustment_pct': adjustment_pct,
        'verdict': 'Aggressive Allocation' if kelly_pct > 0.15 else 'Conservative' if kelly_pct < 0.08 else 'Moderate'
    }


def calculate_win_rate(returns: pd.Series, threshold: float = 0) -> dict:
    """
    Calculate historical win rate from returns.
    
    Args:
        returns: Daily returns series
        threshold: Minimum return to count as "win"
    
    Returns:
        Dict with win rate and related stats
    """
    returns = returns.dropna()
    
    winning = returns[returns > threshold]
    losing = returns[returns <= threshold]
    
    win_rate = len(winning) / len(returns) if len(returns) > 0 else 0.5
    avg_win = float(winning.mean()) if len(winning) > 0 else 0.01
    avg_loss = float(abs(losing.mean())) if len(losing) > 0 else 0.01
    
    return {
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'win_loss_ratio': avg_win / avg_loss if avg_loss > 0 else 1.0,
        'sample_size': len(returns)
    }


def calculate_model_confidence(recent_predictions: list, recent_actuals: list) -> dict:
    """
    Track rolling accuracy to detect model staleness.
    
    Fix #2: If accuracy drops below 55%, warn that model may be stale
    due to market regime shift.
    
    Args:
        recent_predictions: List of recent predictions (0/1 or probabilities)
        recent_actuals: List of actual outcomes (0/1)
    
    Returns:
        Dict with confidence level and any warnings
    """
    if len(recent_predictions) < 3:
        return {
            'confidence': 'UNKNOWN',
            'accuracy': 0.0,
            'warning': 'Insufficient data for confidence assessment'
        }
    
    # Convert to arrays
    preds = np.array(recent_predictions)
    actuals = np.array(recent_actuals)
    
    # Handle probability predictions (convert to binary)
    if preds.dtype == float:
        preds = (preds > 0.5).astype(int)
    
    # Calculate rolling accuracy
    accuracy = np.mean(preds == actuals)
    
    # Determine confidence level
    if accuracy < 0.55:
        return {
            'confidence': 'LOW',
            'accuracy': float(accuracy),
            'warning': 'Model may be stale - market regime shifted'
        }
    elif accuracy < 0.60:
        return {
            'confidence': 'MEDIUM',
            'accuracy': float(accuracy),
            'warning': None
        }
    else:
        return {
            'confidence': 'HIGH',
            'accuracy': float(accuracy),
            'warning': None
        }


def calculate_hurst_exponent(prices: pd.Series, max_lag: int = 100) -> float:
    """
    Calculate Hurst Exponent using R/S Analysis.
    
    H > 0.5: Trending (momentum works)
    H < 0.5: Mean-reverting (contrarian works)
    H = 0.5: Random walk
    
    Args:
        prices: Price series
        max_lag: Maximum lag for R/S analysis
    
    Returns:
        Hurst exponent (0-1)
    """
    prices = prices.dropna()
    
    if len(prices) < max_lag:
        max_lag = len(prices) // 2
    
    if max_lag < 10:
        return 0.5  # Not enough data
    
    lags = range(10, max_lag)
    tau = []
    
    for lag in lags:
        # Calculate spread
        diffs = np.subtract(prices.iloc[lag:].values, prices.iloc[:-lag].values)
        tau.append(np.std(diffs))
    
    # Linear fit in log-log space
    try:
        poly = np.polyfit(np.log(list(lags)), np.log(tau), 1)
        H = poly[0]
        return float(np.clip(H, 0, 1))
    except:
        return 0.5


if __name__ == "__main__":
    print("=" * 60)
    print("TRADYXA RUBIX - RISK CALCULATOR TEST")
    print("=" * 60)
    
    # Test with sample returns
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0.001, 0.015, 500))
    
    # Test VaR
    var_result = calculate_var_cvar(returns)
    print(f"\nVaR/CVaR (Fix #8 uses r={get_risk_free_rate():.0%}):")
    print(f"  VaR 95%: {var_result['var_95']:.2%}")
    print(f"  VaR 99%: {var_result['var_99']:.2%}")
    print(f"  CVaR 95%: {var_result['cvar_95']:.2%}")
    
    # Test Kelly
    win_stats = calculate_win_rate(returns)
    kelly_result = kelly_regime_adjusted(
        win_stats['win_rate'], 
        'TRENDING', 
        win_stats['avg_win'], 
        win_stats['avg_loss']
    )
    print(f"\nKelly Criterion (Fix #4 - Regime Adjusted):")
    print(f"  Base win rate: {kelly_result['base_win_rate']:.1%}")
    print(f"  Adjusted (TRENDING): {kelly_result['adjusted_win_rate']:.1%}")
    print(f"  Kelly fraction: {kelly_result['kelly_pct']}")
    print(f"  Verdict: {kelly_result['verdict']}")
    
    # Test model confidence
    preds = [1, 0, 1, 1, 0]
    actuals = [1, 0, 0, 1, 1]
    conf = calculate_model_confidence(preds, actuals)
    print(f"\nModel Confidence (Fix #2):")
    print(f"  Accuracy: {conf['accuracy']:.1%}")
    print(f"  Confidence: {conf['confidence']}")
    if conf['warning']:
        print(f"  ⚠️ Warning: {conf['warning']}")
