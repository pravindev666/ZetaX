#!/usr/bin/env python3
"""
Tradyxa RubiX - GBM Divergence Detector
Detects RSI/MACD divergences using Gradient Boosting Machine
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

# Model directory
MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def train_gbm_divergence(features_df: pd.DataFrame) -> dict:
    """
    Train GBM to detect RSI/MACD divergences.
    
    Bullish Divergence: Price makes lower low, RSI makes higher low
    Bearish Divergence: Price makes higher high, RSI makes lower high
    
    Args:
        features_df: DataFrame with features
    
    Returns:
        Dict with model and training stats
    """
    print("Training GBM Divergence Detector...")
    
    df = features_df.copy()
    
    # Detect divergence patterns
    df['price_5d_min'] = df['Close'].rolling(5).min()
    df['price_5d_max'] = df['Close'].rolling(5).max()
    df['rsi_5d_min'] = df['rsi_14'].rolling(5).min()
    df['rsi_5d_max'] = df['rsi_14'].rolling(5).max()
    
    # Bullish divergence: price lower low, RSI higher low
    df['bullish_div'] = (
        (df['price_5d_min'] < df['price_5d_min'].shift(5)) &
        (df['rsi_5d_min'] > df['rsi_5d_min'].shift(5))
    ).astype(int)
    
    # Bearish divergence: price higher high, RSI lower high
    df['bearish_div'] = (
        (df['price_5d_max'] > df['price_5d_max'].shift(5)) &
        (df['rsi_5d_max'] < df['rsi_5d_max'].shift(5))
    ).astype(int)
    
    # Target: Any divergence
    df['divergence'] = (df['bullish_div'] | df['bearish_div']).astype(int)
    
    # Feature columns
    feature_cols = [
        'rsi_14', 'macd', 'macd_histogram',
        'return_5d', 'return_20d',
        'bb_position', 'volume_ratio'
    ]
    
    # Drop NaN
    df = df.dropna(subset=feature_cols + ['divergence'])
    
    X = df[feature_cols]
    y = df['divergence']
    
    print(f"  Training samples: {len(X)}")
    print(f"  Divergence rate: {y.mean():.1%}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    
    # Train GBM
    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    
    print(f"  Train accuracy: {train_acc:.1%}")
    print(f"  Test accuracy: {test_acc:.1%}")
    
    # Package for saving
    model_package = {
        'model': model,
        'feature_cols': feature_cols,
        'train_accuracy': train_acc,
        'test_accuracy': test_acc,
        'training_samples': len(X_train)
    }
    
    # Save model
    model_path = MODELS_DIR / "gbm_divergence.pkl"
    joblib.dump(model_package, model_path)
    print(f"  ✅ Saved to: {model_path}")
    
    return model_package


def infer_divergence(features_df: pd.DataFrame, model_path: str = None) -> dict:
    """
    Detect divergence for current day.
    
    Args:
        features_df: DataFrame with features
        model_path: Path to model .pkl file
    
    Returns:
        Dict with divergence detection results
    """
    # Load model
    if model_path is None:
        model_path = MODELS_DIR / "gbm_divergence.pkl"
    
    data = joblib.load(model_path)
    model = data['model']
    feature_cols = data['feature_cols']
    
    # Get latest row
    latest = features_df[feature_cols].iloc[-1:]
    
    # Get prediction
    prob = model.predict_proba(latest)[0][1]
    detected = prob > 0.5
    
    # Determine type (bullish or bearish) from RSI direction
    rsi = features_df['rsi_14'].iloc[-1]
    price_trend = features_df['return_5d'].iloc[-1]
    
    if detected:
        if rsi > 50 and price_trend < 0:
            div_type = 'BULLISH'
            verdict = 'Price weak but RSI holding - potential reversal UP'
        elif rsi < 50 and price_trend > 0:
            div_type = 'BEARISH'
            verdict = 'Price strong but RSI weak - potential reversal DOWN'
        else:
            div_type = 'MIXED'
            verdict = 'Divergence detected but unclear direction'
    else:
        div_type = 'NONE'
        verdict = 'No divergence - trend alignment normal'
    
    return {
        'detected': detected,
        'probability': float(prob),
        'type': div_type,
        'verdict': verdict
    }


if __name__ == "__main__":
    print("=" * 60)
    print("TRADYXA RUBIX - GBM DIVERGENCE TRAINING")
    print("=" * 60)
    
    # Test with sample data
    from data_fetcher import fetch_recent_data
    from feature_builder import build_features
    
    nifty = fetch_recent_data("^NSEI", "5y")
    vix = fetch_recent_data("^INDIAVIX", "5y")
    
    features = build_features(nifty, vix)
    
    # Train
    result = train_gbm_divergence(features)
    
    # Test inference
    print("\n" + "-" * 40)
    print("Testing inference on latest data:")
    div = infer_divergence(features)
    print(f"  Detected: {div['detected']}")
    print(f"  Type: {div['type']}")
    print(f"  Verdict: {div['verdict']}")
