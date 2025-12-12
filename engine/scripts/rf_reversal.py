#!/usr/bin/env python3
"""
Tradyxa RubiX - Random Forest Streak Reversal
Predicts probability of streak reversal after consecutive up/down days

=== Fix #5: Streak Confidence Penalty ===
Streaks > 5 days are rare in training data (few samples).
We cap streak at 5 for modeling and apply exponential confidence penalty
for longer streaks to avoid overconfident predictions on rare events.
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Model directory
MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def train_rf_reversal(features_df: pd.DataFrame, labels_df: pd.DataFrame = None) -> dict:
    """
    Train Random Forest to predict streak reversal.
    
    Target: Will tomorrow reverse the current streak?
    Features: Streak length, RSI, VIX, volatility, etc.
    
    Args:
        features_df: DataFrame with features
        labels_df: Optional DataFrame with labels (if None, creates them)
    
    Returns:
        Dict with model and training stats
    """
    print("Training RF Streak Reversal...")
    
    df = features_df.copy()
    
    # Create reversal label if not provided
    df['next_return_sign'] = np.sign(df['return_1d'].shift(-1))
    df['streak_sign'] = np.sign(df['streak'])
    df['reversal'] = (df['streak_sign'] != df['next_return_sign']).astype(int)
    
    # Feature columns
    feature_cols = [
        'streak', 'rsi_14', 'bb_position', 'macd_histogram',
        'volatility_20d', 'vix', 'vix_percentile',
        'atr_pct', 'volume_ratio', 'price_vs_sma20'
    ]
    
    # Drop NaN and last row (no future data for label)
    df = df.dropna(subset=feature_cols + ['reversal'])
    df = df.iloc[:-1]  # Remove last row (can't verify reversal)
    
    # ================================================================
    # Fix #5: Cap streak for modeling (rare events beyond 5)
    # ================================================================
    df['streak_capped'] = df['streak'].clip(-5, 5)
    feature_cols_capped = ['streak_capped' if c == 'streak' else c for c in feature_cols]
    
    X = df[feature_cols_capped]
    y = df['reversal']
    
    print(f"  Training samples: {len(X)}")
    print(f"  Reversal rate: {y.mean():.1%}")
    
    # Train-test split (time-series aware: no shuffle)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    
    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    
    print(f"  Train accuracy: {train_acc:.1%}")
    print(f"  Test accuracy: {test_acc:.1%}")
    
    # Feature importances
    importances = dict(zip(feature_cols_capped, model.feature_importances_))
    
    # Package for saving
    model_package = {
        'model': model,
        'feature_cols': feature_cols_capped,
        'original_feature_cols': feature_cols,
        'train_accuracy': train_acc,
        'test_accuracy': test_acc,
        'feature_importances': importances,
        'training_samples': len(X_train),
        'base_reversal_rate': float(y.mean())
    }
    
    # Save model
    model_path = MODELS_DIR / "rf_reversal.pkl"
    joblib.dump(model_package, model_path)
    print(f"  ✅ Saved to: {model_path}")
    
    return model_package


def calculate_streak_reversal(streak: int, features: pd.DataFrame, model_path: str = None) -> dict:
    """
    Calculate streak reversal probability with confidence penalty.
    
    Fix #5: For streaks > 5, we apply exponential confidence decay
    because the model has fewer training samples for rare long streaks.
    
    Args:
        streak: Current streak value (positive=up, negative=down)
        features: DataFrame with feature values for current day
        model_path: Path to model .pkl file
    
    Returns:
        Dict with reversal probability, confidence, and adjusted probability
    """
    # Load model
    if model_path is None:
        model_path = MODELS_DIR / "rf_reversal.pkl"
    
    data = joblib.load(model_path)
    model = data['model']
    feature_cols = data['feature_cols']
    
    # Prepare features
    X = features[feature_cols].values.reshape(1, -1)
    
    # Get raw prediction
    raw_prob = model.predict_proba(X)[0][1]  # Probability of reversal
    
    # ================================================================
    # Fix #5: Confidence penalty for rare long streaks
    # ================================================================
    adjusted_prob = raw_prob
    confidence = 'HIGH'
    
    abs_streak = abs(streak)
    if abs_streak > 5:
        # Exponential decay: 0.9^(streak-5) per extra day
        confidence_penalty = 0.9 ** (abs_streak - 5)
        adjusted_prob = raw_prob * confidence_penalty
        confidence = 'LOW' if abs_streak > 7 else 'MEDIUM'
    
    return {
        'raw_probability': float(raw_prob),
        'adjusted_probability': float(adjusted_prob),
        'confidence': confidence,
        'current_streak': streak,
        'streak_capped': min(abs_streak, 5),
        'is_rare_streak': abs_streak > 5
    }


def infer_reversal(features_df: pd.DataFrame, model_path: str = None) -> dict:
    """
    Predict streak reversal for current day.
    
    Args:
        features_df: DataFrame with features
        model_path: Path to model .pkl file
    
    Returns:
        Dict with reversal prediction
    """
    # Load model
    if model_path is None:
        model_path = MODELS_DIR / "rf_reversal.pkl"
    
    data = joblib.load(model_path)
    model = data['model']
    feature_cols = data['feature_cols']
    
    # Get latest row
    latest = features_df.iloc[-1:]
    
    # Get current streak
    current_streak = int(latest['streak'].iloc[0])
    
    # Cap streak for model input
    latest_capped = latest.copy()
    if 'streak_capped' not in latest_capped.columns:
        latest_capped['streak_capped'] = latest['streak'].clip(-5, 5)
    
    # Adjust feature columns
    X = latest_capped[feature_cols]
    
    # Get prediction
    result = calculate_streak_reversal(current_streak, latest_capped, model_path)
    
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("TRADYXA RUBIX - RF REVERSAL TRAINING")
    print("=" * 60)
    
    # Test with sample data
    from data_fetcher import fetch_recent_data
    from feature_builder import build_features
    
    nifty = fetch_recent_data("^NSEI", "5y")
    vix = fetch_recent_data("^INDIAVIX", "5y")
    
    features = build_features(nifty, vix)
    
    # Train
    result = train_rf_reversal(features)
    
    # Test inference
    print("\n" + "-" * 40)
    print("Testing inference on latest data:")
    reversal = infer_reversal(features)
    print(f"  Current streak: {reversal['current_streak']}")
    print(f"  Reversal probability: {reversal['adjusted_probability']:.1%}")
    print(f"  Confidence: {reversal['confidence']}")
