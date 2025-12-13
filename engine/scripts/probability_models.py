#!/usr/bin/env python3
"""
Tradyxa RubiX - Probability Models
Monte Carlo, Jump Diffusion, and Barrier Breach calculations

=== Fix #7: Estimated Jump Parameters ===
Instead of hardcoding lambda_j, mu_j, sigma_j for Merton Jump Diffusion,
we estimate them from historical data by identifying "jumps" (returns > 2 std).
"""

import numpy as np
import pandas as pd
from scipy.stats import norm


def estimate_jump_parameters(returns: pd.Series) -> tuple:
    """
    Estimate Merton jump parameters from historical returns.
    
    Fix #7: Instead of hardcoded parameters, we derive them from data.
    
    A "jump" is defined as a return > 2 standard deviations.
    
    Args:
        returns: Series of daily returns
    
    Returns:
        Tuple of (lambda_j, mu_j, sigma_j)
        - lambda_j: Annual jump frequency
        - mu_j: Mean jump size
        - sigma_j: Jump size std deviation
    """
    returns = returns.dropna()
    threshold = 2 * returns.std()
    
    # Identify jumps (extreme moves)
    jumps = returns[abs(returns) > threshold]
    
    # Parameters
    if len(jumps) > 0:
        lambda_j = len(jumps) / len(returns) * 252  # Annualized frequency
        mu_j = float(jumps.mean())
        sigma_j = float(jumps.std()) if len(jumps) > 1 else 0.02
    else:
        # Defaults if no jumps detected
        lambda_j = 5.0  # ~5 jumps per year
        mu_j = 0.0
        sigma_j = 0.02
    
    return lambda_j, mu_j, sigma_j


def merton_jump_diffusion_simulation(
    S0: float,
    r: float,
    sigma: float,
    T: float,
    returns: pd.Series = None,
    n_paths: int = 10000
) -> np.ndarray:
    """
    Merton (1976) Jump-Diffusion Model simulation.
    
    Fix #7: Jump parameters estimated from data if returns provided.
    
    Args:
        S0: Current spot price
        r: Risk-free rate
        sigma: Continuous volatility (annualized)
        T: Time to expiry (in years)
        returns: Historical returns for jump parameter estimation
        n_paths: Number of simulation paths
    
    Returns:
        Array of simulated prices at time T
    """
    # Get jump parameters
    if returns is not None:
        lambda_j, mu_j, sigma_j = estimate_jump_parameters(returns)
    else:
        # Defaults
        lambda_j, mu_j, sigma_j = 5.0, 0.0, 0.02
    
    # Ensure sigma_j is not zero
    sigma_j = max(sigma_j, 0.01)
    
    # Number of jumps (Poisson)
    n_jumps = np.random.poisson(lambda_j * T, n_paths)
    
    # Jump component
    jump_component = np.zeros(n_paths)
    for i in range(n_paths):
        if n_jumps[i] > 0:
            jumps = np.random.normal(mu_j, sigma_j, n_jumps[i])
            jump_component[i] = np.sum(jumps)
    
    # Drift adjustment for jumps
    k = np.exp(mu_j + 0.5 * sigma_j**2) - 1
    drift = (r - 0.5 * sigma**2 - lambda_j * k) * T
    
    # Diffusion component
    diffusion = sigma * np.sqrt(T) * np.random.normal(0, 1, n_paths)
    
    # Final prices
    ST = S0 * np.exp(drift + diffusion + jump_component)
    
    return ST


def prob_touch_barrier(spot: float, barrier: float, sigma: float, T: float, r: float = 0.07) -> float:
    """
    Probability of price touching a barrier level (Goldman Sachs style).
    
    Uses Black-Scholes barrier probability formula.
    
    Args:
        spot: Current spot price
        barrier: Barrier level
        sigma: Annualized volatility
        T: Time in years
        r: Risk-free rate
    
    Returns:
        Probability [0, 1]
    """
    if sigma <= 0 or T <= 0:
        return 0.0
    
    # Drift mu for the process ln(S)
    mu = r - 0.5 * sigma**2
    
    # Standard deviation over time T
    vol_sqrt_t = sigma * np.sqrt(T)
    
    # Log moneyness
    log_s_b = np.log(spot / barrier)
    
    if barrier > spot:  # Up barrier (Call-like)
        # Probability of hitting H > S
        # P = N( (ln(S/H) + mu*T) / vol_T ) + (H/S)^(2mu/sigma^2) * N( (ln(S/H) - mu*T) / vol_T ) -- NO wait
        # Correct formula for P(Max >= H) with drift mu:
        
        lambda_param = 2 * mu / (sigma**2)
        
        # x term
        x = (log_s_b + mu * T) / vol_sqrt_t
        
        # y term (reflected)
        # We need N( (ln(S/H) - mu*T) / ... ) ?
        # Actually standard result:
        # P = N( (ln(S/H) - |mu|T)/... ) ? No.
        
        # Let's use the standard "One Touch" analytic formula:
        # Reversal of d2?
        
        # Analytic solution for First Passage Time <= T:
        # A = ( -log(B/S) + mu*T ) / (sigma*sqrt(T))
        # B = ( -log(B/S) - mu*T ) / (sigma*sqrt(T))
        # Prob = N(B) + (B/S)^(2mu/sigma^2) * N(A)  <-- Common form
        
        # Let's map it:
        # Target H = barrier. Start S = spot.
        # log_H_S = log(barrier/spot)
        log_b_s = np.log(barrier / spot) # Positive
        
        term1 = (-log_b_s + mu * T) / vol_sqrt_t
        term2 = (-log_b_s - mu * T) / vol_sqrt_t
        
        prob = norm.cdf(term2) + (barrier / spot)**(lambda_param) * norm.cdf(term1)
        
    else:  # Down barrier (Put-like) H < S
        # Symmetry: Map S -> 1/S, H -> 1/H, mu -> -mu ?
        # Or just use the formula with correct signs
        
        log_s_b = np.log(spot / barrier) # Positive
        lambda_param = 2 * mu / (sigma**2)
        
        # For down barrier, we need Min <= H.
        # Similar structure but signs flipped.
        
        log_s_b = np.log(spot/barrier) # Positive
        
        # term1 = ( -log(S/B) + mu*T ) / ...
        term1 = (-log_s_b + mu * T) / vol_sqrt_t
        term2 = (-log_s_b - mu * T) / vol_sqrt_t
        
        prob = norm.cdf(term2) + (spot / barrier)**(-lambda_param) * norm.cdf(term1)

    return float(np.clip(prob, 0.0, 1.0))


def monte_carlo_cones(spot: float, sigma: float, T_days: int = 5, n_paths: int = 10000, returns: pd.Series = None) -> dict:
    """
    Generate Monte Carlo price cones at 1σ, 2σ, 3σ levels.
    
    Args:
        spot: Current spot price
        sigma: Annualized volatility
        T_days: Projection period in days
        n_paths: Number of simulation paths
        returns: Historical returns for jump estimation
    
    Returns:
        Dict with cone levels for each day
    """
    cones = {}
    r = 0.07  # Risk-free rate
    
    for day in range(1, T_days + 1):
        T = day / 252  # Convert to years
        
        # Run simulation
        paths = merton_jump_diffusion_simulation(spot, r, sigma, T, returns, n_paths)
        
        # Calculate percentiles
        cones[f'day_{day}'] = {
            '3sigma_low': float(np.percentile(paths, 0.15)),   # ~3σ down
            '2sigma_low': float(np.percentile(paths, 2.5)),   # ~2σ down
            '1sigma_low': float(np.percentile(paths, 16)),    # ~1σ down
            'median': float(np.percentile(paths, 50)),
            '1sigma_high': float(np.percentile(paths, 84)),   # ~1σ up
            '2sigma_high': float(np.percentile(paths, 97.5)), # ~2σ up
            '3sigma_high': float(np.percentile(paths, 99.85)) # ~3σ up
        }
    
    return {
        'spot': spot,
        'sigma': sigma,
        'cones': cones
    }


def calculate_probability_surface(spot: float, vix: float, returns: pd.Series = None) -> dict:
    """
    Calculate probability surface for different price levels.
    
    Args:
        spot: Current spot price
        vix: Current VIX level
        returns: Historical returns for parameter estimation
    
    Returns:
        Dict with probabilities for various moves
    """
    sigma = vix / 100  # VIX as annualized vol proxy
    sigma = max(sigma, 0.10)  # Minimum 10% vol
    
    # One-day probabilities
    T = 1/252
    paths = merton_jump_diffusion_simulation(spot, 0.07, sigma, T, returns, 10000)
    
    moves = {
        'up_1pct': float(np.mean(paths > spot * 1.01)),
        'up_2pct': float(np.mean(paths > spot * 1.02)),
        'down_1pct': float(np.mean(paths < spot * 0.99)),
        'down_2pct': float(np.mean(paths < spot * 0.98)),
        'within_1pct': float(np.mean(abs(paths/spot - 1) < 0.01)),
    }
    
    # Call/Put skew
    call_bias = moves['up_1pct'] / (moves['up_1pct'] + moves['down_1pct'] + 1e-6)
    
    return {
        'probabilities': moves,
        'call_bias': float(call_bias),
        'put_bias': float(1 - call_bias),
        'skew': 'Call Bias' if call_bias > 0.55 else 'Put Bias' if call_bias < 0.45 else 'Neutral'
    }


if __name__ == "__main__":
    print("=" * 60)
    print("TRADYXA RUBIX - PROBABILITY MODELS TEST")
    print("=" * 60)
    
    # Test with sample data
    import yfinance as yf
    
    nifty = yf.download("^NSEI", period="1y", progress=False)
    returns = nifty['Close'].pct_change().dropna()
    spot = float(nifty['Close'].iloc[-1])
    
    # Test jump parameter estimation
    lambda_j, mu_j, sigma_j = estimate_jump_parameters(returns)
    print(f"\nJump Parameters (Fix #7):")
    print(f"  Lambda (freq): {lambda_j:.2f} jumps/year")
    print(f"  Mu (mean): {mu_j:.4f}")
    print(f"  Sigma (std): {sigma_j:.4f}")
    
    # Test Monte Carlo
    vix = 12.0
    cones = monte_carlo_cones(spot, vix/100, T_days=5, returns=returns)
    print(f"\nMonte Carlo Cones (spot={spot:.0f}):")
    for day, levels in cones['cones'].items():
        print(f"  {day}: {levels['1sigma_low']:.0f} - {levels['1sigma_high']:.0f} (1σ)")
    
    # Test barrier probability
    barrier_up = spot * 1.02
    prob = prob_touch_barrier(spot, barrier_up, vix/100, 5/252)
    print(f"\nBarrier Breach Probability:")
    print(f"  P(touch {barrier_up:.0f}) in 5 days: {prob:.1%}")
