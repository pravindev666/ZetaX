#!/usr/bin/env python3
"""
Tradyxa RubiX - Weekly Model Training Script
Runs every Saturday via GitHub Actions

Trains all 5 ML models on 20 years of NIFTY/VIX data:
1. HMM Regime Detector
2. RF Streak Reversal
3. XGBoost Momentum
4. Quantile Regression Range
5. GBM Divergence
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from data_fetcher import fetch_all_training_data, DATA_DIR
from feature_builder import build_features
from hmm_regime import train_hmm_regime
from rf_reversal import train_rf_reversal
from xgb_momentum import train_xgb_momentum
from qr_range import train_qr_range
from gbm_divergence import train_gbm_divergence


def main():
    """Main training orchestration function."""
    print("=" * 60)
    print("TRADYXA RUBIX - WEEKLY MODEL TRAINING")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Step 1: Fetch Historical Data
    print("\n[1/7] Fetching historical data from yfinance...")
    print("      This may take a few minutes for 20 years of data...")
    
    try:
        nifty, banknifty, vix = fetch_all_training_data()
        print(f"      NIFTY: {len(nifty)} rows")
        print(f"      BANKNIFTY: {len(banknifty)} rows")
        print(f"      VIX: {len(vix)} rows")
    except Exception as e:
        print(f"      ❌ Error fetching data: {e}")
        sys.exit(1)
    
    # Step 2: Build Features
    print("\n[2/7] Building features from OHLCV + VIX data...")
    features_df = build_features(nifty, vix)
    print(f"      Generated {len(features_df.columns)} features")
    print(f"      Training samples: {len(features_df)}")
    
    # Step 3: Train HMM Regime
    print("\n[3/7] Training HMM Regime Detector...")
    try:
        train_hmm_regime(features_df)
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Step 4: Train RF Reversal
    print("\n[4/7] Training Random Forest Reversal...")
    try:
        train_rf_reversal(features_df)
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Step 5: Train XGB Momentum
    print("\n[5/7] Training XGBoost Momentum...")
    try:
        train_xgb_momentum(features_df)
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Step 6: Train QR Range
    print("\n[6/7] Training Quantile Regression Range...")
    try:
        train_qr_range(features_df)
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Step 7: Train GBM Divergence
    print("\n[7/7] Training GBM Divergence...")
    try:
        train_gbm_divergence(features_df)
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Summary
    models_dir = SCRIPTS_DIR.parent / "models"
    model_files = list(models_dir.glob("*.pkl"))
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print(f"Models saved to: {models_dir}")
    print(f"Model files: {len(model_files)}")
    for f in model_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  - {f.name}: {size_mb:.2f} MB")
    print(f"Finished at: {datetime.now().isoformat()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
