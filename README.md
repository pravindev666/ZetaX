# Tradyxa RubiX

> **AI-Powered Market Intelligence Dashboard for NIFTY & BANKNIFTY**

[![Live Demo](https://img.shields.io/badge/Live-Demo-00f3ff?style=for-the-badge)](https://tradyxa-rubix.pages.dev)
[![License](https://img.shields.io/badge/License-Proprietary-ff3333?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://python.org)
[![React](https://img.shields.io/badge/React-19-61dafb?style=for-the-badge&logo=react)](https://react.dev)

---

## 🎯 What is Tradyxa RubiX?

Tradyxa RubiX is a **free, AI-powered trading analytics dashboard** that provides actionable insights for NIFTY and BANKNIFTY traders. It combines 5 Machine Learning models with statistical analysis to generate **19 dynamic tiles** with plain-English verdicts.

**Key Features:**
- 🤖 5 ML Models trained on 3000+ days of historical data
- 📊 19 Real-time tiles updated every inference run
- 🎯 Plain-English verdicts for beginners
- 📈 Monte Carlo simulations with 10,000 price paths
- 🔄 Automated daily updates via GitHub Actions

---

## 📐 System Architecture

```mermaid
flowchart TB
    subgraph DATA["📦 Data Layer"]
        YF[("Yahoo Finance API")]
        CSV[(Cached CSV Files)]
    end
    
    subgraph ML["🤖 ML Engine (Python)"]
        DF[data_fetcher.py]
        FB[feature_builder.py]
        
        subgraph MODELS["Trained Models"]
            HMM[HMM Regime Detector]
            RF[RF Streak Reversal]
            XGB[XGBoost Momentum]
            QR[Quantile Regression]
            GBM[GBM Divergence]
        end
        
        STATS[Statistical Formulas]
        INFER[infer.py]
    end
    
    subgraph OUTPUT["📤 Output"]
        JSON[(rubix_nifty.json<br>rubix_banknifty.json)]
    end
    
    subgraph FRONTEND["🖥️ Frontend (React)"]
        APP[App.tsx]
        TILES[19 Dashboard Tiles]
        VERDICT[Overall Verdict]
    end
    
    YF --> DF
    DF --> CSV
    CSV --> FB
    FB --> MODELS
    MODELS --> INFER
    STATS --> INFER
    INFER --> JSON
    JSON --> APP
    APP --> TILES
    APP --> VERDICT
```

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI Framework with Hooks |
| **TypeScript** | Type-safe JavaScript |
| **Tailwind CSS** | Utility-first styling |
| **Framer Motion** | Animations |
| **Recharts** | Chart visualizations |
| **Lucide Icons** | Icon library |

### Backend (ML Engine)
| Technology | Purpose |
|------------|---------|
| **Python 3.12** | ML & Data Processing |
| **yfinance** | Market data fetching |
| **pandas** | Data manipulation |
| **numpy** | Numerical computing |
| **scikit-learn** | RandomForest, QuantileRegression |
| **xgboost** | Gradient Boosting |
| **hmmlearn** | Hidden Markov Models |
| **scipy** | Statistical functions |
| **joblib** | Model serialization |

### DevOps
| Technology | Purpose |
|------------|---------|
| **GitHub Actions** | CI/CD automation |
| **Cloudflare Pages** | Frontend hosting |
| **Cron Schedules** | Automated training/inference |

---

## 📁 Project Structure

```
Tradyxa-Rubix/
├── 📂 engine/                    # Python ML Backend
│   ├── 📂 scripts/               # All Python scripts
│   │   ├── data_fetcher.py       # yfinance data ingestion
│   │   ├── feature_builder.py    # 68 technical features
│   │   ├── hmm_regime.py         # HMM Regime Detector
│   │   ├── rf_reversal.py        # RF Streak Reversal
│   │   ├── xgb_momentum.py       # XGBoost Momentum
│   │   ├── qr_range.py           # Quantile Regression Range
│   │   ├── gbm_divergence.py     # GBM Divergence Detector
│   │   ├── probability_models.py # Monte Carlo, barriers
│   │   ├── risk_calculator.py    # VaR, Kelly, CVaR
│   │   ├── friday_fear.py        # Weekend gap analysis
│   │   ├── train_all_models.py   # Weekly training orchestrator
│   │   └── infer.py              # Daily inference → JSON
│   ├── 📂 data/                  # Cached market data CSVs
│   ├── 📂 models/                # Trained .pkl files
│   └── requirements.txt          # Python dependencies
│
├── 📂 public/
│   └── 📂 data/
│       ├── rubix_nifty.json      # NIFTY inference output
│       └── rubix_banknifty.json  # BANKNIFTY inference output
│
├── 📂 components/                # React UI components
├── 📂 services/                  # Data fetching services
├── 📂 .github/workflows/         # GitHub Actions
│   ├── weekly_training.yml       # Saturday model training
│   └── daily_inference.yml       # Hourly inference updates
│
├── App.tsx                       # Main React component
├── types.ts                      # TypeScript interfaces
├── index.html                    # Entry point with meta tags
└── README.md                     # This file
```

---

## 🤖 Machine Learning Models

### Overview

```mermaid
flowchart LR
    subgraph INPUT["Raw Data"]
        OHLCV[OHLCV Prices]
        VIX[India VIX]
    end
    
    subgraph FEATURES["68 Features"]
        RSI[RSI 14]
        MACD[MACD]
        BB[Bollinger Bands]
        ATR[ATR 14]
        SMA[SMA 20/50/200]
        VOL[Volatility]
        STREAK[Streak Days]
    end
    
    subgraph MODELS["5 ML Models"]
        M1["🔴 HMM Regime"]
        M2["🟢 RF Reversal"]
        M3["🔵 XGB Momentum"]
        M4["🟡 QR Range"]
        M5["🟣 GBM Divergence"]
    end
    
    INPUT --> FEATURES
    FEATURES --> MODELS
```

---

### Model 1: HMM Regime Detector

**File:** `engine/scripts/hmm_regime.py`

**Purpose:** Identifies the current market regime (TRENDING, MEAN_REVERTING, or CHAOTIC)

**Algorithm:** Gaussian Hidden Markov Model with 3 hidden states

**How It Works:**
```mermaid
sequenceDiagram
    participant Data as Historical Returns
    participant HMM as HMM Model
    participant States as Hidden States
    participant Output as Regime Label
    
    Data->>HMM: Daily returns (3000+ days)
    HMM->>States: Fit Gaussian HMM (3 states)
    States->>HMM: Sort by volatility
    Note over States: State 0 = Low Vol (Trending)
    Note over States: State 1 = Med Vol (Mean-Rev)
    Note over States: State 2 = High Vol (Chaotic)
    HMM->>Output: Predict current state
    Output-->>Dashboard: "TRENDING" / "MEAN_REVERTING" / "CHAOTIC"
```

**Training Data:** 
- Source: yfinance `^NSEI` (NIFTY 50)
- Period: 2005-01-01 to present
- Features: Daily log returns

**State Labeling (Fix #6):**
States are sorted by volatility to ensure consistent labeling:
- Lowest volatility → TRENDING
- Medium volatility → MEAN_REVERTING  
- Highest volatility → CHAOTIC

**Dashboard Tile:** `Market Regime`

---

### Model 2: Random Forest Streak Reversal

**File:** `engine/scripts/rf_reversal.py`

**Purpose:** Predicts probability of trend reversal after winning/losing streaks

**Algorithm:** Random Forest Classifier (100 trees)

**Features Used:**
| Feature | Description |
|---------|-------------|
| `streak_length` | Consecutive up/down days |
| `streak_return` | Cumulative return during streak |
| `rsi_14` | Relative Strength Index |
| `bb_position` | Position within Bollinger Bands |
| `volume_ratio` | Volume vs 20-day average |

**How It Works:**
```mermaid
flowchart TD
    A[Current Streak: 5 up days] --> B{RF Model}
    B --> C[Predict: 65% reversal probability]
    C --> D{Streak > 5 days?}
    D -->|Yes| E[Apply exponential penalty]
    D -->|No| F[Use raw probability]
    E --> G[Adjusted: 45% confidence]
    F --> G
    G --> H[Verdict: Low/Medium/High reversal chance]
```

**Streak Confidence Penalty (Fix #5):**
```python
if streak > 5:
    penalty = 0.85 ** (streak - 5)
    probability *= penalty
```

**Dashboard Tile:** `Reversal Chance`

---

### Model 3: XGBoost Momentum Pulse

**File:** `engine/scripts/xgb_momentum.py`

**Purpose:** Scores momentum strength from 0-100

**Algorithm:** XGBoost Classifier with gradient boosting

**Features Used (15 total):**
```python
['return_1d', 'return_5d', 'return_10d', 'return_20d',
 'volatility_20d', 'rsi_14', 'macd', 'macd_signal', 'macd_hist',
 'bb_position', 'atr_14', 'sma_ratio_20_50', 'vix', 
 'volume_ratio', 'streak']
```

**Score Interpretation:**
| Score | Verdict |
|-------|---------|
| > 70 | STRONG MOMENTUM - Trend continuation likely |
| 50-70 | MODERATE - Be selective |
| < 50 | WEAK/RANGE-BOUND - Avoid trend trades |

**Dashboard Tile:** `Momentum`

---

### Model 4: Quantile Regression Range Predictor

**File:** `engine/scripts/qr_range.py`

**Purpose:** Predicts expected price range with confidence intervals

**Algorithm:** Gradient Boosting Regressor with quantile loss

**Quantiles Predicted:**
- Q10 (10th percentile) → Lower bound
- Q50 (50th percentile) → Median
- Q90 (90th percentile) → Upper bound

**Skewness Adjustment (Fix #9):**
```mermaid
flowchart LR
    A[Calculate Skewness] --> B{Skew > 0.5?}
    B -->|Yes| C[Expand upper range 1.2x]
    B -->|No| D{Skew < -0.5?}
    D -->|Yes| E[Expand lower range 1.2x]
    D -->|No| F[Use symmetric ranges]
```

**Dashboard Tile:** `Expected Range`

---

### Model 5: GBM Divergence Detector

**File:** `engine/scripts/gbm_divergence.py`

**Purpose:** Detects price-indicator divergences (bullish/bearish)

**Algorithm:** Gradient Boosting Machine Classifier

**Divergence Types:**
| Type | Condition |
|------|-----------|
| **Bullish** | Price making lower lows, RSI making higher lows |
| **Bearish** | Price making higher highs, RSI making lower highs |
| **None** | No divergence detected |

**Dashboard Tiles:** `hero.verdictTitle` (BULLISH EDGE / BEARISH DIVERGENCE)

---

## 📊 Tile-to-Model Mapping

```mermaid
flowchart TB
    subgraph ML_TILES["🤖 ML Model Tiles"]
        T1[Market Regime] --> M1[HMM]
        T2[Reversal Chance] --> M2[RF]
        T3[Momentum] --> M3[XGB]
        T4[Expected Range] --> M4[QR]
        T5[Hero Verdict] --> M5[GBM]
    end
    
    subgraph STAT_TILES["📈 Statistical Tiles"]
        T6[VIX] --> S1[Live yfinance]
        T7[Max Daily Loss] --> S2[VaR Formula]
        T8[Bet Size] --> S3[Kelly Criterion]
        T9[Trend Strength] --> S4[Hurst Exponent]
        T10[5d Prediction] --> S5[Monte Carlo]
        T11[Touch Probability] --> S6[Barrier Formula]
        T12[Weekend Risk] --> S7[Friday Analysis]
    end
    
    subgraph LIVE_TILES["🔴 Live Data Tiles"]
        T13[Current Level] --> L1[yfinance ^NSEI]
        T14[VIX Term] --> L2[vix_5d vs vix_20d]
        T15[Time Decay] --> L3[Theta Estimation]
        T16[Expiry Pin] --> L4[Round to 100]
        T17[Support Level] --> L5[Volume Ratio]
        T18[Next Event] --> L6[datetime.weekday]
    end
    
    subgraph COMPOSITE["🎯 Composite Tiles"]
        T19[System Status] --> C1[Traffic Light Score]
        T20[Greed Meter] --> C2[FOMO Formula]
        T21[Overall Verdict] --> C3[Signal Counter]
    end
```

---

## 🔄 Data Flow Pipeline

### Weekly Training Flow

```mermaid
sequenceDiagram
    participant GH as GitHub Actions
    participant DF as data_fetcher.py
    participant YF as Yahoo Finance
    participant FB as feature_builder.py
    participant TRAIN as train_all_models.py
    participant MODELS as models/*.pkl
    
    rect rgb(40, 40, 60)
        Note over GH: Every Saturday 00:00 UTC
        GH->>DF: Trigger training
        DF->>YF: Fetch NIFTY (2005-present)
        DF->>YF: Fetch BANKNIFTY
        DF->>YF: Fetch VIX
        YF-->>DF: OHLCV data
        DF->>FB: Process raw data
        FB->>FB: Generate 68 features
        FB->>TRAIN: Feature matrix
        TRAIN->>TRAIN: Train HMM
        TRAIN->>TRAIN: Train RF
        TRAIN->>TRAIN: Train XGB
        TRAIN->>TRAIN: Train QR
        TRAIN->>TRAIN: Train GBM
        TRAIN->>MODELS: Save .pkl files
        MODELS-->>GH: Commit to repo
    end
```

### Daily Inference Flow

```mermaid
sequenceDiagram
    participant GH as GitHub Actions
    participant INFER as infer.py
    participant YF as Yahoo Finance
    participant FB as feature_builder.py
    participant MODELS as models/*.pkl
    participant JSON as rubix_*.json
    participant FE as React Frontend
    
    rect rgb(40, 60, 40)
        Note over GH: Every 30 min (M-F 9:15-15:30 IST)
        GH->>INFER: Trigger inference
        INFER->>YF: Fetch last 1 year data
        INFER->>YF: Get live price
        YF-->>INFER: 26,046 (NIFTY)
        INFER->>FB: Build features
        FB-->>INFER: 68-feature vector
        INFER->>MODELS: Load trained models
        MODELS-->>INFER: Predictions
        Note over INFER: HMM → TRENDING
        Note over INFER: XGB → Score 45
        Note over INFER: RF → 39% reversal
        INFER->>INFER: Run statistical calcs
        Note over INFER: VaR: -1.1%
        Note over INFER: Kelly: 5%
        Note over INFER: MC: 25647-26495
        INFER->>JSON: Write rubix_nifty.json
        JSON-->>GH: Commit to repo
        GH-->>FE: Deploy to Cloudflare
        FE->>JSON: Fetch latest data
        FE->>FE: Render 19 tiles
    end
```

---

## 📊 Feature Engineering

### 68 Technical Features

**File:** `engine/scripts/feature_builder.py`

```mermaid
flowchart LR
    subgraph PRICE["Price Features (12)"]
        P1[return_1d]
        P2[return_5d]
        P3[return_10d]
        P4[return_20d]
        P5[log_return]
        P6[high_low_range]
        P7[close_open_range]
        P8[gap]
        P9[body_size]
        P10[upper_wick]
        P11[lower_wick]
        P12[body_position]
    end
    
    subgraph TREND["Trend Features (8)"]
        T1[sma_20]
        T2[sma_50]
        T3[sma_200]
        T4[ema_12]
        T5[ema_26]
        T6[sma_ratio_20_50]
        T7[price_sma_ratio]
        T8[streak]
    end
    
    subgraph MOMENTUM["Momentum Features (8)"]
        M1[rsi_14]
        M2[macd]
        M3[macd_signal]
        M4[macd_hist]
        M5[stoch_k]
        M6[stoch_d]
        M7[williams_r]
        M8[cci]
    end
    
    subgraph VOL["Volatility Features (10)"]
        V1[volatility_5d]
        V2[volatility_10d]
        V3[volatility_20d]
        V4[bb_upper]
        V5[bb_lower]
        V6[bb_width]
        V7[bb_position]
        V8[atr_14]
        V9[atr_pct]
        V10[keltner_position]
    end
```

**Feature Leakage Prevention (Fix #1):**
```python
# Labels use future data (shift -1)
df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

# Features use only past data (no shift or positive shift)
df['return_1d'] = df['Close'].pct_change(1)  # Uses yesterday
```

---

## 📈 Statistical Formulas

### Value at Risk (VaR)

```python
def calculate_var_cvar(returns, confidence=0.95):
    """Historical VaR at 95% confidence."""
    var = np.percentile(returns, (1 - confidence) * 100)
    cvar = returns[returns <= var].mean()
    return {'var_95': var, 'cvar_95': cvar}
```

### Kelly Criterion (Regime-Adjusted)

```python
def kelly_regime_adjusted(win_rate, regime, avg_win, avg_loss):
    """
    Kelly = (p * b - q) / b
    Where: p = win_rate, q = 1-p, b = avg_win/avg_loss
    """
    b = avg_win / abs(avg_loss) if avg_loss != 0 else 1
    kelly = (win_rate * b - (1 - win_rate)) / b
    
    # Regime adjustment (Fix #4)
    if regime == 'CHAOTIC':
        kelly *= 0.5  # Halve in chaotic markets
    elif regime == 'MEAN_REVERTING':
        kelly *= 0.8  # Reduce in ranging markets
    
    return max(0, min(kelly, 0.25))  # Cap at 25%
```

### Hurst Exponent

```python
def calculate_hurst_exponent(prices, max_lag=100):
    """
    H > 0.5: Trending (momentum works)
    H < 0.5: Mean-reverting (contrarian works)
    H = 0.5: Random walk
    """
    lags = range(2, min(max_lag, len(prices) // 2))
    tau = [np.std(np.subtract(prices[lag:], prices[:-lag])) for lag in lags]
    hurst = np.polyfit(np.log(lags), np.log(tau), 1)[0]
    return hurst / 2
```

### Monte Carlo Simulation

```python
def monte_carlo_cones(spot, volatility, T_days=5, n_sims=10000):
    """Merton Jump-Diffusion Monte Carlo."""
    dt = 1/252
    paths = np.zeros((n_sims, T_days))
    paths[:, 0] = spot
    
    for t in range(1, T_days):
        z = np.random.standard_normal(n_sims)
        jump = np.random.poisson(jump_lambda * dt, n_sims)
        paths[:, t] = paths[:, t-1] * np.exp(
            (mu - 0.5 * volatility**2) * dt +
            volatility * np.sqrt(dt) * z +
            jump * jump_mean
        )
    
    return {
        '1sigma_low': np.percentile(paths[:, -1], 16),
        'median': np.median(paths[:, -1]),
        '1sigma_high': np.percentile(paths[:, -1], 84)
    }
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/pravindev666/ZetaX.git
cd ZetaX

# Install Python dependencies
cd engine
pip install -r requirements.txt

# Train models (first time only)
python scripts/train_all_models.py

# Run inference
python scripts/infer.py

# Start frontend (in root directory)
cd ..
npm install
npm run dev
```

### Running Locally

```bash
# Terminal 1: Run inference
cd engine
python scripts/infer.py

# Terminal 2: Start dev server
npm run dev
# Opens http://localhost:5173
```

---

## 🔧 GitHub Actions

### Weekly Training (`weekly_training.yml`)

```yaml
schedule:
  - cron: '0 0 * * 6'  # Saturday 00:00 UTC
```

**Steps:**
1. Fetch latest NIFTY/BANKNIFTY/VIX data
2. Train all 5 ML models
3. Commit updated `.pkl` files

### Daily Inference (`daily_inference.yml`)

```yaml
schedule:
  - cron: '*/30 4-10 * * 1-5'  # Every 30 min, M-F, 9:30-16:00 IST
```

**Steps:**
1. Fetch live prices
2. Run inference pipeline
3. Generate `rubix_nifty.json` and `rubix_banknifty.json`
4. Commit and deploy

---

## 📜 Legal & Compliance

### SEBI Compliance Statement

> ⚠️ **IMPORTANT DISCLAIMER**
>
> Tradyxa RubiX is an **educational analytics tool** and does not provide financial advice. All predictions are probabilistic estimates based on historical data.
>
> - Past performance does not guarantee future results
> - Trade at your own risk
> - We are not SEBI registered investment advisors
> - This is NOT a recommendation to buy/sell securities

### Data Sources

| Source | Usage | License |
|--------|-------|---------|
| Yahoo Finance | OHLCV, VIX data | Fair Use |
| NSE India | Reference only | Public Data |

---

## 👥 Credits

**Developed by:** Zeta Aztra Technologies (India)

**Contact:** zetaaztratech@gmail.com

**Jurisdiction:** Chennai, Tamil Nadu, India

---

## 📄 License

Copyright © 2025 Zeta Aztra Technologies. All Rights Reserved.

This software is proprietary. Unauthorized copying, modification, or distribution is prohibited.

---

<div align="center">
  <img src="public/favicon.png" width="64" alt="Tradyxa RubiX Logo">
  <h3>Tradyxa RubiX</h3>
  <p><em>AI-Powered Market Intelligence</em></p>
</div>
