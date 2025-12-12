#!/usr/bin/env python3
"""
Tradyxa RubiX - HMM Regime Detector
Hidden Markov Model for market regime classification

=== Fix #6: Stable State Labeling ===
HMM states can flip labels between training runs.
We force consistent labeling by sorting states by volatility:
- Lowest volatility = TRENDING
- Middle volatility = MEAN_REVERTING  
- Highest volatility = CHAOTIC

The state mapping is saved in the .pkl file for inference consistency.
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from hmmlearn import hmm

# Model directory
MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def train_hmm_regime(features_df: pd.DataFrame) -> dict:
    """
    Train Hidden Markov Model for market regime detection.
    
    States:
        TRENDING: Low volatility, strong directional moves
        MEAN_REVERTING: Medium volatility, oscillating
        CHAOTIC: High volatility, unpredictable
    
    Args:
        features_df: DataFrame with features (must have return_1d, volatility_20d)
    
    Returns:
        Dict with model, state_labels, and training stats
    """
    print("Training HMM Regime Detector...")
    
    # Prepare observations
    observations = features_df[['return_1d', 'volatility_20d']].values
    
    # Handle any remaining NaN
    mask = ~np.isnan(observations).any(axis=1)
    observations = observations[mask]
    
    print(f"  Training samples: {len(observations)}")
    
    # Initialize HMM with 3 hidden states
    model = hmm.GaussianHMM(
        n_components=3,
        covariance_type="full",
        n_iter=1000,
        random_state=42,
        verbose=False
    )
    
    # Train the model
    model.fit(observations)
    
    # Get state sequence
    hidden_states = model.predict(observations)
    
    # ================================================================
    # Fix #6: Force consistent state labeling by volatility
    # ================================================================
    # Sort states by their volatility mean (index 1 in observations)
    vol_means = [model.means_[i][1] for i in range(3)]
    sorted_indices = np.argsort(vol_means)
    
    # Create state label mapping (lowest vol = TRENDING, highest = CHAOTIC)
    state_labels = [''] * 3
    state_labels[sorted_indices[0]] = 'TRENDING'
    state_labels[sorted_indices[1]] = 'MEAN_REVERTING'
    state_labels[sorted_indices[2]] = 'CHAOTIC'
    
    # Create reverse mapping for inference
    label_to_state = {label: i for i, label in enumerate(state_labels)}
    
    # Calculate transition matrix probabilities
    transition_matrix = model.transmat_
    
    # Calculate state statistics
    state_stats = {}
    for i in range(3):
        state_mask = hidden_states == i
        state_stats[state_labels[i]] = {
            'mean_return': float(observations[state_mask, 0].mean()) if state_mask.sum() > 0 else 0,
            'mean_volatility': float(observations[state_mask, 1].mean()) if state_mask.sum() > 0 else 0,
            'frequency': float(state_mask.sum() / len(hidden_states)),
            'state_index': i
        }
    
    # Package everything for saving
    model_package = {
        'model': model,
        'state_labels': state_labels,
        'label_to_state': label_to_state,
        'transition_matrix': transition_matrix.tolist(),
        'state_stats': state_stats,
        'training_samples': len(observations),
        'scaler_mean': observations.mean(axis=0).tolist(),
        'scaler_std': observations.std(axis=0).tolist()
    }
    
    # Save model
    model_path = MODELS_DIR / "hmm_regime.pkl"
    joblib.dump(model_package, model_path)
    print(f"  ✅ Saved to: {model_path}")
    
    # Print state info
    print("\n  State Labels (by volatility):")
    for label in ['TRENDING', 'MEAN_REVERTING', 'CHAOTIC']:
        stats = state_stats[label]
        print(f"    {label}: mean_vol={stats['mean_volatility']:.4f}, freq={stats['frequency']:.1%}")
    
    return model_package


def infer_regime(features_df: pd.DataFrame, model_path: str = None) -> dict:
    """
    Predict current market regime using the trained HMM.
    
    Args:
        features_df: DataFrame with current features
        model_path: Path to model .pkl file (optional)
    
    Returns:
        Dict with regime, probability, and all state probabilities
    """
    # Load model
    if model_path is None:
        model_path = MODELS_DIR / "hmm_regime.pkl"
    
    data = joblib.load(model_path)
    model = data['model']
    state_labels = data['state_labels']
    
    # Get latest observation
    latest = features_df[['return_1d', 'volatility_20d']].iloc[-1:].values
    
    # Handle NaN
    if np.isnan(latest).any():
        return {
            'regime': 'UNKNOWN',
            'probability': 0.0,
            'all_probabilities': {label: 0.0 for label in ['TRENDING', 'MEAN_REVERTING', 'CHAOTIC']},
            'error': 'NaN in features'
        }
    
    # Predict regime
    state = model.predict(latest)[0]
    probs = model.predict_proba(latest)[0]
    
    # Map to labels
    current_regime = state_labels[state]
    
    return {
        'regime': current_regime,
        'probability': float(probs[state]),
        'all_probabilities': {
            state_labels[i]: float(probs[i]) for i in range(3)
        },
        'state_stats': data.get('state_stats', {})
    }


if __name__ == "__main__":
    print("=" * 60)
    print("TRADYXA RUBIX - HMM REGIME TRAINING")
    print("=" * 60)
    
    # Test with sample data
    from data_fetcher import fetch_recent_data
    from feature_builder import build_features
    
    nifty = fetch_recent_data("^NSEI", "2y")
    vix = fetch_recent_data("^INDIAVIX", "2y")
    
    features = build_features(nifty, vix)
    
    # Train
    result = train_hmm_regime(features)
    
    # Test inference
    print("\n" + "-" * 40)
    print("Testing inference on latest data:")
    regime = infer_regime(features)
    print(f"  Current regime: {regime['regime']} ({regime['probability']:.1%})")
