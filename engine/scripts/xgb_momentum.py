#!/usr/bin/env python3
"""
Tradyxa RubiX - XGBoost Momentum Pulse
Predicts momentum strength (0-100) for next 1-3 days
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# Model directory
MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def train_xgb_momentum(features_df: pd.DataFrame) -> dict:
    """
    Train XGBoost to score momentum strength.
    
    Target: Strong momentum (>1.5% move) in next 3 days
    Output: Probability score 0-100
    
    Args:
        features_df: DataFrame with features
    
    Returns:
        Dict with model and training stats
    """
    print("Training XGB Momentum Pulse...")
    
    df = features_df.copy()
    
    # Create momentum label: Strong directional move in next 3 days
    df['future_3d_return'] = df['Close'].shift(-3) / df['Close'] - 1
    df['strong_momentum'] = (abs(df['future_3d_return']) > 0.015).astype(int)
    
    # Feature columns
    feature_cols = [
        'rsi_14', 'macd', 'macd_histogram', 'bb_position',
        'return_1d', 'return_5d', 'return_20d',
        'volatility_10d', 'volatility_20d',
        'atr_pct', 'volume_ratio',
        'price_vs_sma20', 'price_vs_sma50',
        'vix', 'vix_percentile', 'vix_term_structure'
    ]
    
    # Drop NaN and future-looking rows
    df = df.dropna(subset=feature_cols + ['strong_momentum'])
    df = df.iloc[:-3]  # Remove last 3 rows (no future data)
    
    X = df[feature_cols]
    y = df['strong_momentum']
    
    print(f"  Training samples: {len(X)}")
    print(f"  Strong momentum rate: {y.mean():.1%}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    
    # Train XGBoost
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss',
        verbosity=0
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    
    print(f"  Train accuracy: {train_acc:.1%}")
    print(f"  Test accuracy: {test_acc:.1%}")
    
    # Feature importances
    importances = dict(zip(feature_cols, model.feature_importances_))
    
    # Package for saving
    model_package = {
        'model': model,
        'feature_cols': feature_cols,
        'train_accuracy': train_acc,
        'test_accuracy': test_acc,
        'feature_importances': importances,
        'training_samples': len(X_train)
    }
    
    # Save model
    model_path = MODELS_DIR / "xgb_momentum.pkl"
    joblib.dump(model_package, model_path)
    print(f"  ✅ Saved to: {model_path}")
    
    return model_package


def infer_momentum(features_df: pd.DataFrame, model_path: str = None) -> dict:
    """
    Predict momentum score for current day.
    
    Args:
        features_df: DataFrame with features
        model_path: Path to model .pkl file
    
    Returns:
        Dict with momentum score (0-100), strength classification
    """
    # Load model
    if model_path is None:
        model_path = MODELS_DIR / "xgb_momentum.pkl"
    
    data = joblib.load(model_path)
    model = data['model']
    feature_cols = data['feature_cols']
    
    # Get latest row
    latest = features_df[feature_cols].iloc[-1:]
    
    # Get probability
    prob = model.predict_proba(latest)[0][1]
    score = int(prob * 100)
    
    # Classify strength
    if prob > 0.7:
        strength = 'HIGH'
        verdict = 'Strong momentum expected'
    elif prob > 0.4:
        strength = 'MEDIUM'
        verdict = 'Moderate momentum'
    else:
        strength = 'LOW'
        verdict = 'Weak/Range-bound'
    
    return {
        'score': score,
        'probability': float(prob),
        'strength': strength,
        'verdict': verdict
    }


if __name__ == "__main__":
    print("=" * 60)
    print("TRADYXA RUBIX - XGB MOMENTUM TRAINING")
    print("=" * 60)
    
    # Test with sample data
    from data_fetcher import fetch_recent_data
    from feature_builder import build_features
    
    nifty = fetch_recent_data("^NSEI", "5y")
    vix = fetch_recent_data("^INDIAVIX", "5y")
    
    features = build_features(nifty, vix)
    
    # Train
    result = train_xgb_momentum(features)
    
    # Test inference
    print("\n" + "-" * 40)
    print("Testing inference on latest data:")
    momentum = infer_momentum(features)
    print(f"  Momentum score: {momentum['score']}")
    print(f"  Strength: {momentum['strength']}")
    print(f"  Verdict: {momentum['verdict']}")
