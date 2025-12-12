#!/usr/bin/env python3
"""
Tradyxa RubiX - Quantile Regression Range Predictor
Predicts price range quartiles (Q10, Q25, Q50, Q75, Q90) for next day

=== Fix #9: Skewness-Adjusted Ranges ===
Markets are often asymmetric (crashes faster than rallies).
We detect skewness in recent returns and expand the relevant tail:
- Negative skew → Expand downside range (Q10 wider)
- Positive skew → Expand upside range (Q90 wider)
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.linear_model import QuantileRegressor

# Model directory
MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def train_qr_range(features_df: pd.DataFrame) -> dict:
    """
    Train Quantile Regression for price range prediction.
    
    Predicts Q10, Q25, Q50, Q75, Q90 of next-day price range as % of close.
    
    Args:
        features_df: DataFrame with features
    
    Returns:
        Dict with models (one per quantile) and training stats
    """
    print("Training Quantile Regression Range...")
    
    df = features_df.copy()
    
    # Create range label: Next-day range as % of close
    df['next_range'] = (df['High'].shift(-1) - df['Low'].shift(-1)) / df['Close']
    
    # Feature columns
    feature_cols = [
        'atr_pct', 'volatility_10d', 'volatility_20d',
        'vix', 'vix_percentile', 'volume_ratio',
        'bb_position', 'rsi_14'
    ]
    
    # Drop NaN
    df = df.dropna(subset=feature_cols + ['next_range'])
    df = df.iloc[:-1]  # Remove last row
    
    X = df[feature_cols]
    y = df['next_range']
    
    print(f"  Training samples: {len(X)}")
    print(f"  Mean range: {y.mean():.2%}")
    
    # Train separate models for each quantile
    quantiles = [0.10, 0.25, 0.50, 0.75, 0.90]
    models = {}
    
    for q in quantiles:
        model = QuantileRegressor(
            quantile=q,
            alpha=0.01,
            solver='highs'
        )
        model.fit(X, y)
        models[f'q{int(q*100)}'] = model
        print(f"    Trained Q{int(q*100)}")
    
    # Package for saving
    model_package = {
        'models': models,
        'feature_cols': feature_cols,
        'quantiles': quantiles,
        'training_samples': len(X),
        'mean_range': float(y.mean()),
        'std_range': float(y.std())
    }
    
    # Save model
    model_path = MODELS_DIR / "qr_range.pkl"
    joblib.dump(model_package, model_path)
    print(f"  ✅ Saved to: {model_path}")
    
    return model_package


def predict_range_with_skew(features_df: pd.DataFrame, model_path: str = None) -> dict:
    """
    Predict range quartiles with skewness adjustment.
    
    Fix #9: Adjust range predictions based on market skew.
    - Negative skew (left tail risk) → Expand downside
    - Positive skew (right tail) → Expand upside
    
    Args:
        features_df: DataFrame with features
        model_path: Path to model .pkl file
    
    Returns:
        Dict with range predictions (Q10-Q90) in points
    """
    # Load model
    if model_path is None:
        model_path = MODELS_DIR / "qr_range.pkl"
    
    data = joblib.load(model_path)
    models = data['models']
    feature_cols = data['feature_cols']
    
    # Get latest row
    latest = features_df[feature_cols].iloc[-1:]
    spot_price = features_df['Close'].iloc[-1]
    
    # Get base predictions
    predictions = {}
    for q_name, qr_model in models.items():
        pred_pct = qr_model.predict(latest)[0]
        predictions[q_name] = pred_pct
    
    # ================================================================
    # Fix #9: Skewness adjustment
    # ================================================================
    # Calculate skew from recent returns
    recent_returns = features_df['return_1d'].iloc[-20:]
    skew = recent_returns.skew()
    
    skew_adjustment = 'NONE'
    
    # Adjust ranges based on skew
    if skew < -0.5:  # Negative skew = expand downside
        predictions['q10'] *= 1.2  # 20% wider downside
        skew_adjustment = 'DOWNSIDE_EXPANDED'
    elif skew > 0.5:  # Positive skew = expand upside
        predictions['q90'] *= 1.2  # 20% wider upside
        skew_adjustment = 'UPSIDE_EXPANDED'
    
    # Convert to points
    range_points = {
        q_name: float(pred_pct * spot_price) 
        for q_name, pred_pct in predictions.items()
    }
    
    return {
        'range_pct': {k: float(v) for k, v in predictions.items()},
        'range_points': range_points,
        'spot_price': float(spot_price),
        'skew': float(skew),
        'skew_adjustment': skew_adjustment,
        'expected_range': f"±{range_points['q50']:.0f} pts (median)"
    }


def infer_range(features_df: pd.DataFrame, model_path: str = None) -> dict:
    """
    Simplified range inference (wrapper for predict_range_with_skew).
    """
    return predict_range_with_skew(features_df, model_path)


if __name__ == "__main__":
    print("=" * 60)
    print("TRADYXA RUBIX - QR RANGE TRAINING")
    print("=" * 60)
    
    # Test with sample data
    from data_fetcher import fetch_recent_data
    from feature_builder import build_features
    
    nifty = fetch_recent_data("^NSEI", "5y")
    vix = fetch_recent_data("^INDIAVIX", "5y")
    
    features = build_features(nifty, vix)
    
    # Train
    result = train_qr_range(features)
    
    # Test inference
    print("\n" + "-" * 40)
    print("Testing inference on latest data:")
    range_pred = infer_range(features)
    print(f"  Spot: {range_pred['spot_price']:.0f}")
    print(f"  Expected range: {range_pred['expected_range']}")
    print(f"  Q10-Q90 (pts): {range_pred['range_points']['q10']:.0f} - {range_pred['range_points']['q90']:.0f}")
    print(f"  Skew adjustment: {range_pred['skew_adjustment']}")
