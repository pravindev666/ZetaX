#!/usr/bin/env python3
"""
Tradyxa RubiX - Feature Builder
Builds 60+ technical features from OHLCV + VIX data

=== FEATURE LEAKAGE AUDIT (Fix #1) ===
SAFE OPERATIONS (past data only):
- .shift(1), .shift(N) where N > 0 → Uses PAST data ✅
- .rolling(N).mean/std() → Uses past N periods ✅
- .ewm(span=N) → Uses exponential weighted past ✅

DANGEROUS OPERATIONS (future data):
- .shift(-1), .shift(-N) → ONLY used for LABELS, never features ❌
- Any operation that uses future prices → FORBIDDEN ❌

All .shift(-N) calls are ONLY in create_labels() function, not build_features()
"""

import numpy as np
import pandas as pd
from typing import Tuple


def build_features(nifty_df: pd.DataFrame, vix_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build 60+ features from NIFTY OHLCV and VIX data.
    
    IMPORTANT: This function uses ONLY past data for features.
    No future data leakage - verified by audit.
    
    Args:
        nifty_df: NIFTY OHLCV DataFrame
        vix_df: VIX OHLCV DataFrame
    
    Returns:
        DataFrame with all features
    """
    df = nifty_df.copy()
    
    # ═══════════════════════════════════════════════════════════════════
    # PRICE-BASED FEATURES (all use past data via positive shifts/rolling)
    # ═══════════════════════════════════════════════════════════════════
    
    # Daily Returns - using PAST data
    df['return_1d'] = df['Close'].pct_change(1)  # ✅ Uses yesterday
    df['return_5d'] = df['Close'].pct_change(5)   # ✅ Uses 5 days ago
    df['return_20d'] = df['Close'].pct_change(20) # ✅ Uses 20 days ago
    
    # Log Returns
    df['log_return'] = np.log(df['Close'] / df['Close'].shift(1))  # ✅ shift(1)
    
    # Volatility (Rolling Std of Returns) - all use rolling past windows
    df['volatility_10d'] = df['return_1d'].rolling(10).std() * np.sqrt(252)  # ✅
    df['volatility_20d'] = df['return_1d'].rolling(20).std() * np.sqrt(252)  # ✅
    df['volatility_60d'] = df['return_1d'].rolling(60).std() * np.sqrt(252)  # ✅
    
    # Volatility compression (ratio of short to long term vol)
    df['vol_compression'] = df['volatility_10d'] / (df['volatility_60d'] + 1e-10)
    
    # ═══════════════════════════════════════════════════════════════════
    # TECHNICAL INDICATORS (all standard implementations using past data)
    # ═══════════════════════════════════════════════════════════════════
    
    # RSI (Relative Strength Index) - 14-day
    delta = df['Close'].diff()  # ✅ diff uses past
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    df['rsi_14'] = 100 - (100 / (1 + gain / (loss + 1e-10)))
    
    # MACD - uses exponential moving averages of past data
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()  # ✅
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()  # ✅
    df['macd'] = ema_12 - ema_26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_histogram'] = df['macd'] - df['macd_signal']
    
    # Bollinger Bands - 20-day rolling
    df['bb_middle'] = df['Close'].rolling(20).mean()  # ✅
    df['bb_std'] = df['Close'].rolling(20).std()      # ✅
    df['bb_upper'] = df['bb_middle'] + 2 * df['bb_std']
    df['bb_lower'] = df['bb_middle'] - 2 * df['bb_std']
    df['bb_position'] = (df['Close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'] + 1e-10)
    df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
    
    # ATR (Average True Range) - 14-day
    high_low = df['High'] - df['Low']
    high_close = abs(df['High'] - df['Close'].shift(1))  # ✅ shift(1)
    low_close = abs(df['Low'] - df['Close'].shift(1))    # ✅ shift(1)
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['atr_14'] = tr.rolling(14).mean()  # ✅
    df['atr_pct'] = df['atr_14'] / df['Close']
    
    # Moving Averages - all rolling past data
    df['sma_5'] = df['Close'].rolling(5).mean()    # ✅
    df['sma_20'] = df['Close'].rolling(20).mean()  # ✅
    df['sma_50'] = df['Close'].rolling(50).mean()  # ✅
    df['sma_200'] = df['Close'].rolling(200).mean() # ✅
    
    # EMA
    df['ema_9'] = df['Close'].ewm(span=9, adjust=False).mean()   # ✅
    df['ema_21'] = df['Close'].ewm(span=21, adjust=False).mean() # ✅
    
    # Price vs Moving Averages
    df['price_vs_sma20'] = (df['Close'] - df['sma_20']) / (df['sma_20'] + 1e-10)
    df['price_vs_sma50'] = (df['Close'] - df['sma_50']) / (df['sma_50'] + 1e-10)
    df['price_vs_sma200'] = (df['Close'] - df['sma_200']) / (df['sma_200'] + 1e-10)
    
    # MA Crossovers (binary flags)
    df['sma_5_above_20'] = (df['sma_5'] > df['sma_20']).astype(int)
    df['sma_20_above_50'] = (df['sma_20'] > df['sma_50']).astype(int)
    
    # Rate of Change
    df['roc_10'] = (df['Close'] - df['Close'].shift(10)) / (df['Close'].shift(10) + 1e-10)  # ✅
    df['roc_20'] = (df['Close'] - df['Close'].shift(20)) / (df['Close'].shift(20) + 1e-10)  # ✅
    
    # ═══════════════════════════════════════════════════════════════════
    # STREAK FEATURES (consecutive up/down days)
    # ═══════════════════════════════════════════════════════════════════
    
    df['up_day'] = (df['return_1d'] > 0).astype(int)
    df['down_day'] = (df['return_1d'] < 0).astype(int)
    
    # Streak counter using cumulative grouping
    df['streak_group'] = (df['up_day'] != df['up_day'].shift(1)).cumsum()
    
    # Calculate signed streak (positive for up, negative for down)
    streak_vals = []
    current_streak = 0
    for i, row in df.iterrows():
        if pd.isna(row['return_1d']):
            streak_vals.append(0)
            continue
        if row['return_1d'] > 0:
            if current_streak >= 0:
                current_streak += 1
            else:
                current_streak = 1
        elif row['return_1d'] < 0:
            if current_streak <= 0:
                current_streak -= 1
            else:
                current_streak = -1
        else:
            current_streak = 0
        streak_vals.append(current_streak)
    
    df['streak'] = streak_vals
    df['streak_abs'] = abs(df['streak'])
    
    # ═══════════════════════════════════════════════════════════════════
    # VIX FEATURES (merge VIX data)
    # ═══════════════════════════════════════════════════════════════════
    
    # Align VIX to NIFTY dates
    df['vix'] = vix_df['Close'].reindex(df.index).ffill()
    df['vix_5d_avg'] = df['vix'].rolling(5).mean()   # ✅
    df['vix_20d_avg'] = df['vix'].rolling(20).mean() # ✅
    df['vix_percentile'] = df['vix'].rolling(252).rank(pct=True)  # ✅
    
    # VIX Term Structure proxy
    df['vix_term_structure'] = (df['vix_20d_avg'] - df['vix_5d_avg']) / (df['vix_20d_avg'] + 1e-10)
    
    # VIX change
    df['vix_change_1d'] = df['vix'].pct_change(1)  # ✅
    df['vix_change_5d'] = df['vix'].pct_change(5)  # ✅
    
    # VIX vs Price correlation
    df['vix_price_corr'] = df['vix'].rolling(20).corr(df['Close'])  # ✅
    
    # ═══════════════════════════════════════════════════════════════════
    # VOLUME FEATURES
    # ═══════════════════════════════════════════════════════════════════
    
    df['volume_sma_20'] = df['Volume'].rolling(20).mean()  # ✅
    df['volume_ratio'] = df['Volume'] / (df['volume_sma_20'] + 1e-10)
    df['volume_change'] = df['Volume'].pct_change(1)  # ✅
    
    # Volume-price relationship
    df['volume_price_corr'] = df['Volume'].rolling(20).corr(df['Close'])  # ✅
    
    # ═══════════════════════════════════════════════════════════════════
    # HIGHER-ORDER FEATURES
    # ═══════════════════════════════════════════════════════════════════
    
    # Momentum indicators
    df['momentum_10'] = df['Close'] - df['Close'].shift(10)  # ✅
    df['momentum_20'] = df['Close'] - df['Close'].shift(20)  # ✅
    
    # Williams %R
    highest_14 = df['High'].rolling(14).max()  # ✅
    lowest_14 = df['Low'].rolling(14).min()    # ✅
    df['williams_r'] = ((highest_14 - df['Close']) / (highest_14 - lowest_14 + 1e-10)) * -100
    
    # Stochastic K
    df['stoch_k'] = ((df['Close'] - lowest_14) / (highest_14 - lowest_14 + 1e-10)) * 100
    df['stoch_d'] = df['stoch_k'].rolling(3).mean()  # ✅
    
    # ADX components (simplified)
    df['plus_dm'] = np.where(
        (df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']),
        np.maximum(df['High'] - df['High'].shift(1), 0),
        0
    )
    df['minus_dm'] = np.where(
        (df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)),
        np.maximum(df['Low'].shift(1) - df['Low'], 0),
        0
    )
    
    # Intraday range features
    df['daily_range_pct'] = (df['High'] - df['Low']) / df['Close']
    df['body_range_ratio'] = abs(df['Close'] - df['Open']) / (df['High'] - df['Low'] + 1e-10)
    
    # Gap feature (today's open vs yesterday's close)
    df['gap_pct'] = (df['Open'] - df['Close'].shift(1)) / (df['Close'].shift(1) + 1e-10)  # ✅
    
    # ═══════════════════════════════════════════════════════════════════
    # DAY OF WEEK FEATURES
    # ═══════════════════════════════════════════════════════════════════
    
    df['day_of_week'] = df.index.dayofweek
    df['is_friday'] = (df['day_of_week'] == 4).astype(int)
    df['is_monday'] = (df['day_of_week'] == 0).astype(int)
    
    # Drop rows with NaN for core features only (not sma_200 which needs 200 days)
    core_features = ['return_1d', 'volatility_20d', 'rsi_14', 'macd', 'bb_position', 
                     'atr_14', 'vix', 'volume_sma_20', 'streak']
    df = df.dropna(subset=[c for c in core_features if c in df.columns])
    
    # Fill remaining NaN with forward fill then 0
    df = df.ffill().fillna(0)
    
    return df


def create_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create target labels for ML models.
    
    IMPORTANT: This function uses .shift(-N) which looks at FUTURE data.
    This is ONLY for creating training labels, NOT features.
    
    Labels are ONLY used during training, never during inference.
    
    Args:
        df: DataFrame with features
    
    Returns:
        DataFrame with added label columns
    """
    # ═══════════════════════════════════════════════════════════════════
    # LABELS FOR TRAINING (uses future data - ONLY for labels)
    # ═══════════════════════════════════════════════════════════════════
    
    # Reversal label: Did the streak reverse next day?
    df['next_return_sign'] = np.sign(df['return_1d'].shift(-1))  # ⚠️ Future - LABEL ONLY
    df['streak_sign'] = np.sign(df['streak'])
    df['label_reversal'] = (df['streak_sign'] != df['next_return_sign']).astype(int)
    
    # Momentum label: Strong move (>1.5%) in next 3 days?
    df['future_3d_return'] = df['Close'].shift(-3) / df['Close'] - 1  # ⚠️ Future - LABEL ONLY
    df['label_strong_momentum'] = (abs(df['future_3d_return']) > 0.015).astype(int)
    
    # Range label: Next day's range as % of close
    df['label_next_range'] = (df['High'].shift(-1) - df['Low'].shift(-1)) / df['Close']  # ⚠️ Future - LABEL ONLY
    
    # Direction label: Next day's direction
    df['label_next_direction'] = (df['return_1d'].shift(-1) > 0).astype(int)  # ⚠️ Future - LABEL ONLY
    
    return df


def get_feature_columns() -> dict:
    """
    Get feature column names for each model.
    
    Returns:
        Dict mapping model name to list of feature columns
    """
    # Common features
    base_features = [
        'rsi_14', 'macd_histogram', 'bb_position', 'atr_pct',
        'volatility_20d', 'volume_ratio', 'vix', 'vix_percentile'
    ]
    
    return {
        'reversal': [
            'streak', 'rsi_14', 'bb_position', 'macd_histogram',
            'volatility_20d', 'vix', 'vix_percentile',
            'atr_pct', 'volume_ratio', 'price_vs_sma20'
        ],
        'momentum': [
            'rsi_14', 'macd', 'macd_histogram', 'bb_position',
            'return_1d', 'return_5d', 'return_20d',
            'volatility_10d', 'volatility_20d',
            'atr_pct', 'volume_ratio',
            'price_vs_sma20', 'price_vs_sma50',
            'vix', 'vix_percentile', 'vix_term_structure'
        ],
        'regime': ['return_1d', 'volatility_20d'],
        'range': [
            'atr_pct', 'volatility_10d', 'volatility_20d',
            'vix', 'vix_percentile', 'volume_ratio',
            'bb_position', 'rsi_14'
        ],
        'divergence': [
            'rsi_14', 'macd', 'macd_histogram',
            'return_5d', 'return_20d',
            'bb_position', 'volume_ratio'
        ]
    }


if __name__ == "__main__":
    print("Feature Builder - Testing")
    print("=" * 40)
    
    # Test with sample data
    import yfinance as yf
    
    nifty = yf.download("^NSEI", period="1y", progress=False)
    vix = yf.download("^INDIAVIX", period="1y", progress=False)
    
    # Flatten MultiIndex if present
    if isinstance(nifty.columns, pd.MultiIndex):
        nifty.columns = nifty.columns.get_level_values(0)
    if isinstance(vix.columns, pd.MultiIndex):
        vix.columns = vix.columns.get_level_values(0)
    
    features = build_features(nifty, vix)
    print(f"Generated {len(features.columns)} features")
    print(f"Sample rows: {len(features)}")
    print(f"\nFeature columns:")
    for col in sorted(features.columns):
        print(f"  - {col}")
