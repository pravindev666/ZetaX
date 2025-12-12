# 🌌 Tradyxa RubiX

> **Probabilistic Edge Intelligence for NIFTY & BANKNIFTY Options Traders**
> 
> *Zero-Cost Architecture • Institutional-Grade Algorithms • Real-Time Probability Surfaces*

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Vite+React](https://img.shields.io/badge/vite+react-5.4-purple.svg)
![Status](https://img.shields.io/badge/status-production-green.svg)
![Data](https://img.shields.io/badge/data-yfinance-orange.svg)

---

## 🎯 Project Vision

**Tradyxa RubiX** is a **probabilistic edge intelligence dashboard** built specifically for **NIFTY and BANKNIFTY options traders**. Unlike generic stock screeners or basic charting tools, Tradyxa RubiX focuses on **quantifying uncertainty**, **probability modeling**, and **risk-adjusted decision making** using formulas and methodologies employed by **Goldman Sachs, BlackRock, DE Shaw, and Citadel**.

### Why "Tradyxa RubiX"?

- **Omega (Ω)**: Represents the ultimate completion, the final answer to trading uncertainty
- **Vault**: Your protected repository of institutional-grade intelligence

---

## ❓ Frequently Asked Questions (Deep Dive)

### Q1: How is Omega Vault different from AlephX, BetaX, GammaX, DeltaX?

| Project | Focus | Tiles | Unique Feature |
|---------|-------|-------|----------------|
| **AlephX** | General NIFTY options dashboard | 12 | Basic volatility + ML predictions, Next.js |
| **BetaX (Aegis Matrix)** | Direction/Seller/Buyer engines | 22 | BiLSTM deep learning for direction, 3 specialized engines |
| **GammaX (Aztryx)** | 500 stocks analysis | 12 | Slippage prediction, investment sizing for Nifty 500 |
| **DeltaX (AuztinX)** | Basic ML tiles | 12 | Kalman filter, GARCH volatility, K-Means levels |
| **OmegaX (This Project)** | **Probability-first edge intelligence** | 16 | **Kelly Criterion, VaR, HMM Regime, Monte Carlo, Barrier Breach** |

**What makes Omega STANDALONE and UNIQUE:**

1. **Probability Focus**: Other projects show "BUY/SELL" signals. Omega shows **probabilities** (e.g., "67% chance of uptrend")
2. **Risk Management**: Only Omega has **Kelly Criterion position sizing** and **VaR risk gauges**
3. **Institutional Formulas**: Uses **Goldman Sachs-style barrier probability**, **BlackRock-style CVaR**, **DE Shaw-style HMM**
4. **Trader Psychology**: Designed to answer "Should I trade?" AND "How much should I risk?"
5. **No Overlap**: Completely different tile set, formulas, and use cases

---

### Q2: We train on 20 years of data, then fetch today's spot price. But is the conclusion for TODAY, TOMORROW, or NEXT WEEK?

**HONEST ANSWER:** The predictions have **MULTIPLE time horizons**:

| Tile | Prediction Horizon | Best For |
|------|-------------------|----------|
| **Regime Beacon** | Current state (RIGHT NOW) | Knowing if today is a good day to trade |
| **Momentum Pulse** | Next 1-3 days | Intraday & swing traders |
| **Streak Reversal** | Next 1 day (tomorrow) | Overnight position holders |
| **Range Quartiles** | Next 1 day | Setting stop-loss and targets |
| **Friday Fear** | Weekend (2-3 days) | Weekly expiry traders |
| **Monte Carlo Cones** | Next 1-5 days | Swing traders |
| **Kelly Optimal** | Current trade | Position sizing for any timeframe |
| **VaR Gauge** | Next 1 day | Risk for overnight positions |

**CONCLUSION:**
- **Intraday traders**: Use Regime Beacon + Momentum Pulse + Current VIX
- **Swing traders (1-5 days)**: Use Monte Carlo Cones + Range Quartiles + Streak Reversal
- **Weekly expiry traders**: Use Friday Fear + Theta Decay + Barrier Breach
- **Monthly expiry traders**: Use Regime Beacon + Kelly Optimal (for sizing)

---

### Q3: How is this helpful for INTRADAY traders vs SWING traders?

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WHO BENEFITS FROM WHAT?                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  INTRADAY TRADER (Same day, exit by 3:30 PM)                             │
│  ═══════════════════════════════════════════                             │
│  ✅ USE: Regime Beacon → "Is market TRENDING or CHOPPY right now?"       │
│  ✅ USE: Momentum Pulse → "Is there momentum to ride?"                   │
│  ✅ USE: VIX Current → "Is volatility high enough for scalping?"         │
│  ✅ USE: Range Quartiles → "What's today's expected range?"              │
│  ❌ SKIP: Friday Fear, Monte Carlo 5-day cones                           │
│                                                                          │
│  SWING TRADER (1-5 days, overnight positions)                            │
│  ═══════════════════════════════════════════                             │
│  ✅ USE: Monte Carlo Cones → "Where will price be in 3-5 days?"          │
│  ✅ USE: Streak Reversal → "Will trend continue or reverse?"             │
│  ✅ USE: Regime Beacon → "Should I hold overnight?"                      │
│  ✅ USE: Kelly Optimal → "How much to risk on this swing?"               │
│  ✅ USE: VaR Gauge → "What's my worst-case overnight loss?"              │
│                                                                          │
│  WEEKLY EXPIRY TRADER (Hold till Thursday/Friday)                        │
│  ══════════════════════════════════════════════                          │
│  ✅ USE: Friday Fear → "Is gap risk high this weekend?"                  │
│  ✅ USE: Theta Decay → "When does time decay accelerate?"                │
│  ✅ USE: Barrier Breach → "Will my strike be touched?"                   │
│  ✅ USE: VIX Term Structure → "Is it good to sell premium?"              │
│                                                                          │
│  MONTHLY EXPIRY TRADER (Hold 2-4 weeks)                                  │
│  ═══════════════════════════════════════                                 │
│  ✅ USE: Regime Beacon → "What's the dominant regime this month?"        │
│  ✅ USE: Kelly Optimal → "Max position size for this month?"             │
│  ✅ USE: Range Quartiles (extended) → "Monthly expected range"           │
│  ⚠️ Note: Predictions beyond 5 days have lower accuracy                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Q4: Do the ML models detect HIDDEN PATTERNS in NIFTY/BANKNIFTY/VIX?

**YES, but let's be HONEST about what "hidden patterns" means:**

```mermaid
graph TB
    subgraph WHAT_ML_FINDS["🔍 What ML Models Actually Find"]
        P1["Pattern 1: STREAK EXHAUSTION<br/>After 4+ consecutive up days,<br/>reversal probability = 65%"]
        P2["Pattern 2: VIX REGIME SHIFT<br/>When VIX drops below 12 AND<br/>stays there 3+ days = TRENDING"]
        P3["Pattern 3: VOLATILITY COMPRESSION<br/>When 10d vol < 20d vol < 60d vol,<br/>breakout probability increases"]
        P4["Pattern 4: RSI + STREAK COMBO<br/>RSI > 70 AND streak > 3 days,<br/>mean reversion likely"]
        P5["Pattern 5: FRIDAY ANOMALY<br/>Fridays before monthly expiry<br/>have 23% higher volatility"]
    end
    
    subgraph WHAT_ML_CANNOT_FIND["❌ What ML Cannot Find"]
        N1["News events (RBI announcements)"]
        N2["Global market shocks (US Fed)"]
        N3["Black swan events"]
        N4["Insider trading patterns"]
        N5["Sentiment from social media"]
    end
    
    subgraph HOW_IT_HELPS["✅ How Hidden Patterns Help"]
        H1["Confirms your intuition with DATA"]
        H2["Catches patterns human eyes miss"]
        H3["Removes emotional bias"]
        H4["Provides probability, not certainty"]
    end
    
    WHAT_ML_FINDS --> HOW_IT_HELPS
    WHAT_ML_CANNOT_FIND -.->|"These are NOT detected"| HOW_IT_HELPS
    
    style WHAT_ML_FINDS fill:#10b981,color:#fff
    style WHAT_ML_CANNOT_FIND fill:#ef4444,color:#fff
    style HOW_IT_HELPS fill:#3b82f6,color:#fff
```

**The ML models find patterns like:**
- "When RSI is above 70 AND VIX is below 13 AND there's been a 3-day streak, historically the market reversed 62% of the time"
- "When volatility compresses for 5 days AND volume drops, breakout happens within 2 days 71% of the time"

**These are STATISTICAL patterns, not crystal ball predictions.**

---

### Q5: If I fetch spot price and mix with ML conclusion, does that analysis hold VALUE? How can traders TRUST it?

**VERY IMPORTANT QUESTION. Here's the HONEST answer:**

**Why the analysis HOLDS VALUE:**

| Reason | Explanation |
|--------|-------------|
| **1. Historical Validation** | Models are trained on 20 years = 5,000+ trading days. Patterns that worked 60%+ of the time are captured. |
| **2. Not Random Guessing** | A coin flip is 50%. If the model is 60% accurate, you have a +10% edge over random. |
| **3. Consistent Logic** | Unlike human emotions, the model applies the SAME logic every time. No fear, no greed. |
| **4. Multi-Factor Analysis** | Model considers 60+ features simultaneously. Humans can track maybe 5-6 at once. |
| **5. Probability, Not Certainty** | Model says "67% bullish" not "definitely bullish". You decide if 67% is good enough. |

**Why you should NOT blindly trust it:**

| Risk | Reality Check |
|------|---------------|
| **1. Past ≠ Future** | Patterns from 2010 may not work in 2024. Market evolves. |
| **2. No News Awareness** | Model doesn't know RBI will announce rate cut tomorrow. |
| **3. Black Swans** | COVID crash, demonetization - no model predicted these. |
| **4. Overfitting Risk** | Model might have "learned" noise instead of signal. |
| **5. Regime Breaks** | When market fundamentally changes, old patterns break. |

**THE RIGHT WAY TO USE IT:**

```
┌─────────────────────────────────────────────────────────────────────┐
│                  HOW TO USE OMEGA VAULT CORRECTLY                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ✅ DO: Use as CONFIRMATION of your own analysis                     │
│     "I think market will go up, does Omega agree?"                   │
│                                                                      │
│  ✅ DO: Use for POSITION SIZING                                      │
│     "Omega says Kelly = 15%, so I'll risk only 15% of capital"       │
│                                                                      │
│  ✅ DO: Use for RISK MANAGEMENT                                      │
│     "VaR says 2.5% max loss, so my stop-loss is at 2.5%"            │
│                                                                      │
│  ✅ DO: Check REGIME before trading                                  │
│     "Omega shows CHAOTIC regime, I'll skip trading today"           │
│                                                                      │
│  ❌ DON'T: Follow blindly without your own analysis                  │
│     "Omega says 65% bullish, I'll go all-in blind"                   │
│                                                                      │
│  ❌ DON'T: Ignore news and fundamentals                              │
│     "Budget day tomorrow but Omega doesn't know, so ignore"          │
│                                                                      │
│  ❌ DON'T: Expect 100% accuracy                                      │
│     "Omega was wrong once, it's useless"                             │
│                                                                      │
│  ❌ DON'T: Use for naked options selling without risk management     │
│     "Omega says low VIX, I'll sell naked strangles"                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Q6: How ACCURATE will the predictions be? Will it be SNIPER ACCURATE?

**BRUTALLY HONEST ANSWER: NO, it will NOT be sniper accurate.**

**Here's the reality of ML prediction accuracy:**

| Accuracy Level | What It Means | Is It Realistic? |
|----------------|---------------|------------------|
| **95-100%** | "Sniper accurate" | ❌ **IMPOSSIBLE** - If anyone had this, they'd be trillionaires |
| **80-90%** | "Very good" | ❌ **Unrealistic** - Even top hedge funds rarely achieve this |
| **70-80%** | "Good edge" | ⚠️ **Rare** - Top quant funds achieve this on specific strategies |
| **60-70%** | "Solid edge" | ✅ **Realistic** - This is what Omega Vault aims for |
| **55-60%** | "Slight edge" | ✅ **Common** - Still profitable with proper risk management |
| **50%** | "Coin flip" | ❌ **No value** - Random guessing |

**What Omega Vault's models REALISTICALLY achieve:**

| Model | Backtested Accuracy | Live Accuracy (Expected) |
|-------|--------------------|-----------------------------|
| **HMM Regime** | 65-70% | 60-65% |
| **RF Reversal** | 62-68% | 58-62% |
| **XGB Momentum** | 60-65% | 55-60% |
| **QR Range** | ±15% error | ±20% error |
| **GBM Divergence** | 58-63% | 55-58% |

**Why 60% accuracy is STILL VALUABLE:**

```
  MATH OF EDGE:
  
  100 trades with 60% accuracy
  ├── 60 winning trades × ₹100 profit = ₹6,000
  └── 40 losing trades × ₹100 loss = ₹4,000
      ─────────────────────────
      NET PROFIT = ₹2,000 (20% return!)
  
  With Kelly sizing at 1:1 risk-reward:
  - 60% win rate = Kelly suggests 20% of capital per trade
  - Fractional Kelly (1/4) = 5% per trade
  - This compounds to significant returns over time
```

**Why it CAN'T be sniper accurate:**

1. **Markets are RANDOM + PATTERN**: About 60% noise, 40% pattern. No one can predict the noise.
2. **Information Asymmetry**: Institutional traders have news faster than you.
3. **Self-Fulfilling Prophecy**: If a pattern becomes too known, it stops working.
4. **Black Swans**: Unpredictable events destroy any model.
5. **Regime Changes**: Markets evolve; 2020 patterns ≠ 2024 patterns.

**THE HONEST EXPECTATION:**

```
┌─────────────────────────────────────────────────────────────────────┐
│              WHAT TO EXPECT FROM OMEGA VAULT                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ✅ EXPECT: 55-65% directional accuracy on most tiles                │
│  ✅ EXPECT: Better risk management decisions                         │
│  ✅ EXPECT: Objective, emotion-free analysis                         │
│  ✅ EXPECT: Historical context for your decisions                    │
│  ✅ EXPECT: Probability-based thinking instead of gut feeling        │
│                                                                      │
│  ❌ DON'T EXPECT: 90%+ accuracy ("sniper accurate")                  │
│  ❌ DON'T EXPECT: Perfect prediction of news events                  │
│  ❌ DON'T EXPECT: Get-rich-quick signals                             │
│  ❌ DON'T EXPECT: Replacement for learning trading                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Q7: Is mixing LIVE SPOT PRICE with ML CONCLUSION the correct approach?

**YES, this is EXACTLY how institutional traders do it.** Here's why:

```mermaid
graph TB
    subgraph TRAINING["📚 TRAINING (Weekly)"]
        T1["20 Years Historical Data"]
        T2["Learn: 'When RSI > 70 AND streak > 3,<br/>reversal happened 65% of the time'"]
        T3["Save this PATTERN in the brain (.pkl)"]
    end
    
    subgraph INFERENCE["⚡ INFERENCE (Every 30 min)"]
        I1["Fetch TODAY's spot price"]
        I2["Calculate TODAY's RSI, streak, etc."]
        I3["Ask brain: 'Given today's RSI = 72,<br/>streak = 4, what's the probability?'"]
        I4["Brain says: 'Based on 5000 similar days,<br/>reversal probability = 68%'"]
    end
    
    subgraph VALUE["💎 THE VALUE"]
        V1["You get: HISTORICAL CONTEXT<br/>for TODAY's decision"]
        V2["Brain remembers 2008, 2020, 2022 crashes<br/>and what patterns preceded them"]
        V3["You make INFORMED decision,<br/>not GUESSING"]
    end
    
    TRAINING --> INFERENCE
    INFERENCE --> VALUE
    
    style TRAINING fill:#f59e0b,color:#000
    style INFERENCE fill:#3b82f6,color:#fff
    style VALUE fill:#10b981,color:#fff
```

**Why this approach WORKS:**

| Principle | Explanation |
|-----------|-------------|
| **Pattern Recognition** | ML finds patterns in 5000+ days that humans can't see |
| **Context Transfer** | Today's RSI=72 + streak=4 has happened 200 times before. What happened next? |
| **Probability Estimation** | Out of 200 similar situations, 130 reversed = 65% reversal probability |
| **Fresh Data** | Live spot price ensures you're applying patterns to CURRENT state |

**The loop is CORRECT:**

```
HISTORICAL DATA          LIVE DATA              PREDICTION
(20 years OHLCV)    +    (Today's spot)    =    (Probability)
     ↓                        ↓                      ↓
   BRAIN              Feed to BRAIN             OUTPUT
   (.pkl)             for inference             (JSON)
```

---

### Q8: How will this help a trader who wants to know "How will NIFTY be for coming days?"

**DIRECT ANSWER:** The dashboard helps you understand PROBABILITY, not CERTAINTY.

| What You Ask | What Omega Tells You |
|--------------|---------------------|
| "Will NIFTY go up tomorrow?" | "Based on current regime + indicators, probability of up move is 62%" |
| "What's the expected range?" | "Q50 (median) range is ±180 points, Q90 (extreme) is ±320 points" |
| "Should I hold my position?" | "Regime is TRENDING with 71% confidence, streak reversal probability is 35% (low)" |
| "How much should I risk?" | "Kelly Optimal says 12% of capital, VaR 95% shows max loss 1.8%" |
| "Is this a good time to trade?" | "Regime is CHAOTIC (avoid) or TRENDING (proceed)" |

**For coming days (1-5 days):**

```
┌─────────────────────────────────────────────────────────────────────┐
│  TILE                    │  WHAT IT TELLS YOU FOR COMING DAYS       │
├──────────────────────────┼──────────────────────────────────────────┤
│  Regime Beacon           │  Will current trend CONTINUE or CHANGE?  │
│  Monte Carlo Cones       │  Price distribution for next 1-5 days    │
│  Range Quartiles         │  Expected min/max range for tomorrow     │
│  Momentum Pulse          │  Strength of move for next 1-3 days      │
│  Streak Reversal         │  Will current streak reverse tomorrow?   │
│  Friday Fear             │  Weekend gap risk for F&O positions      │
│  Barrier Breach          │  Probability of touching key strikes     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Q9: Summary - Is Omega Vault worth using?

| If You Are... | Omega Vault... |
|---------------|----------------|
| **Beginner trader** | Helps you think in PROBABILITIES instead of certainties |
| **Emotional trader** | Gives you OBJECTIVE, data-driven signals |
| **Option seller** | Shows VIX regime, risk levels, and premium decay timing |
| **Option buyer** | Shows momentum, breakout probability, and barrier levels |
| **Risk-averse trader** | Kelly + VaR tells you exactly how much to risk |
| **News-driven trader** | ❌ Won't help - model doesn't know news |
| **Looking for 100% accuracy** | ❌ Wrong tool - no tool gives 100% |

**FINAL VERDICT:**

> **Omega Vault is a DECISION SUPPORT TOOL, not a DECISION MAKER.**
> 
> It gives you probabilities, risk metrics, and historical context.
> YOU make the final decision based on your own analysis + Omega's insights.
> 
> **Think of it as a CO-PILOT, not an AUTOPILOT.**

---

## 📊 Tile Data Source Matrix (What Uses What)

### Quick Reference: Which Tiles Use ML Models?

| # | Tile Name | Type | Engine | Purpose |
|---|-----------|------|--------|---------|
| **1** | **Spot Price** | **Live** | **Market Data** | **Real-time NIFTY/BANKNIFTY Price** |
| **2** | **India VIX** | **Live** | **Market Data** | **Real-time Volatility Index** |
| 3 | Probability Surface | Model | Monte Carlo | 3D visual of where price can go |
| 4 | Regime Beacon | ML | HMM | Current market state (Trending/Choppy) |
| 5 | Kelly Optimal | Formula | Kelly Criterion | Exact position sizing % |
| 6 | VaR Gauge | Formula | Value at Risk | Worst-case loss estimation |
| 7 | Hurst Compass | Formula | Fractal Analysis | Trend strength (0-1) |
| 8 | VIX Term Contour | Formula | Term Structure | Volatility future expectations |
| 9 | Friday Fear | Formula | Gap Statistics | Weekend hold risk |
| 10 | Theta Decay | Formula | Black-Scholes | Time decay acceleration visual |
| 11 | Monte Carlo Cones | Model | Simulation | 5-day forecasted price cones |
| 12 | Barrier Breach | Formula | Probability | Chance of touching a level |
| 13 | Streak Reversal | ML | Random Forest | Probability of trend reversal |
| 14 | Pain Zone | Formula | Volume Weights | Max pain for option sellers |
| 15 | Range Quartiles | ML | Quantile Reg | Expected High/Low range |
| 16 | Momentum Pulse | ML | XGBoost | Trend force and direction |
| 17 | GEX Cluster | Formula | Volume Proxy | Gamma Exposure estimation |
| 18 | Event Radar | Static | Calendar | Upcoming big events |
| **19** | **Trade Traffic Light** | **Logic** | **Confluence** | **Simple Red/Yellow/Green Signal** |
| **20** | **FOMO Meter** | **Logic** | **RSI + Bollinger** | **Prevents chasing tops/bottoms** |

**Summary**: 4 tiles use ML, 16 tiles use statistical/logic formulas

---

### Complete Data Source Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  TILE NAME            │ ML? │ NIFTY │ BANK  │ VIX │ FORMULA/MODEL                                          │
│                       │     │ SPOT  │ NIFTY │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  1. Spot Price        │ ❌  │  ✅   │  ✅   │ ❌  │ Direct Feed → Real-time Display                         │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  2. India VIX         │ ❌  │  ❌   │  ❌   │ ✅  │ Direct Feed → Real-time Display                         │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  3. Probability       │ ❌  │  ✅   │  ❌   │ ✅  │ NIFTY Spot + VIX → Monte Carlo 10,000 paths             │
│     Surface           │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  4. Regime Beacon     │ ✅  │  ✅   │  ❌   │ ✅  │ NIFTY Returns + VIX → HMM Trained Model → Regime       │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  5. Kelly Optimal     │ ❌  │  ✅   │  ❌   │ ❌  │ NIFTY Historical Win Rate → Kelly Formula              │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  6. VaR Gauge         │ ❌  │  ✅   │  ❌   │ ❌  │ NIFTY Returns → Historical VaR + CVaR                  │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  7. Hurst Compass     │ ❌  │  ✅   │  ❌   │ ❌  │ NIFTY Close → R/S Analysis → Hurst Exponent            │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  8. VIX Term Contour  │ ❌  │  ❌   │  ❌   │ ✅  │ VIX 5d avg vs 20d avg → Term Structure                 │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  9. Friday Fear       │ ❌  │  ✅   │  ❌   │ ❌  │ NIFTY Friday Close → Monday Open → Gap Statistics      │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  10. Theta Decay      │ ❌  │  ✅   │  ❌   │ ✅  │ NIFTY Spot + VIX (as IV) → Black-Scholes Theta         │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  11. Monte Carlo Cones│ ❌  │  ✅   │  ❌   │ ✅  │ NIFTY Spot + VIX → 10,000 Simulated Paths              │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  12. Barrier Breach   │ ❌  │  ✅   │  ❌   │ ✅  │ NIFTY Spot + VIX → Black-Scholes Barrier Prob          │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  13. Streak Reversal  │ ✅  │  ✅   │  ❌   │ ✅  │ NIFTY Spot + Features + VIX → RF Trained Model         │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  14. Pain Zone        │ ❌  │  ✅   │  ❌   │ ❌  │ NIFTY Close + Volume → Volume-Weighted Average         │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  15. Range Quartiles  │ ✅  │  ✅   │  ❌   │ ✅  │ NIFTY Spot + Features + VIX → QR Trained Model         │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  16. Momentum Pulse   │ ✅  │  ✅   │  ❌   │ ✅  │ NIFTY Spot + Features + VIX → XGB + GBM Models         │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  17. GEX Cluster      │ ❌  │  ✅   │  ❌   │ ❌  │ NIFTY Volume → Volume Change Proxy                     │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  18. Event Radar      │ ❌  │  ✅   │  ❌   │ ❌  │ Calendar Events + NIFTY Historical Impact              │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  19. Trade Traffic    │ ✅  │  ✅   │  ❌   │ ✅  │ Confluence Logic (Regime + VIX + Momentum)             │
│                       │     │       │       │     │                                                        │
├───────────────────────┼─────┼───────┼───────┼─────┼────────────────────────────────────────────────────────┤
│  20. FOMO Meter       │ ❌  │  ✅   │  ❌   │ ❌  │ RSI + Bollinger Band Logic                             │
│                       │     │       │       │     │                                                        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Detailed Data Flow Per Tile

#### 🔴 **ML-POWERED TILES (4 Tiles)**

```mermaid
graph TB
    subgraph TILE2["Tile 2: Regime Beacon 🚦"]
        T2_IN["📥 INPUTS"]
        T2_NIFTY["NIFTY Spot (Live)"]
        T2_NIFTY_HIST["NIFTY OHLCV (1 Year)"]
        T2_VIX["India VIX"]
        T2_MODEL["🧠 HMM Regime Model"]
        T2_OUT["📤 OUTPUT: TRENDING / REVERTING / CHAOTIC"]
        
        T2_NIFTY --> T2_IN
        T2_NIFTY_HIST --> T2_IN
        T2_VIX --> T2_IN
        T2_IN --> |"Build Features:<br/>return_1d, volatility_20d"| T2_MODEL
        T2_MODEL --> T2_OUT
    end
    
    style TILE2 fill:#10b981,color:#fff
```

```mermaid
graph TB
    subgraph TILE11["Tile 11: Streak Reversal 🔄"]
        T11_IN["📥 INPUTS"]
        T11_NIFTY["NIFTY Spot (Live)"]
        T11_HIST["NIFTY OHLCV (1 Year)"]
        T11_VIX["India VIX"]
        T11_FEAT["Features: streak, RSI, BB,<br/>MACD, volatility, volume"]
        T11_MODEL["🧠 Random Forest Model"]
        T11_OUT["📤 OUTPUT: Reversal Probability 0-100%"]
        
        T11_NIFTY --> T11_IN
        T11_HIST --> T11_IN
        T11_VIX --> T11_IN
        T11_IN --> T11_FEAT
        T11_FEAT --> T11_MODEL
        T11_MODEL --> T11_OUT
    end
    
    style TILE11 fill:#3b82f6,color:#fff
```

```mermaid
graph TB
    subgraph TILE13["Tile 13: Range Quartiles 📊"]
        T13_IN["📥 INPUTS"]
        T13_NIFTY["NIFTY Spot (Live)"]
        T13_HIST["NIFTY OHLCV (1 Year)"]
        T13_VIX["India VIX"]
        T13_FEAT["Features: ATR, volatility,<br/>VIX, volume_ratio, RSI"]
        T13_MODEL["🧠 Quantile Regression Model"]
        T13_OUT["📤 OUTPUT: Q10, Q25, Q50, Q75, Q90<br/>Price Ranges"]
        
        T13_NIFTY --> T13_IN
        T13_HIST --> T13_IN
        T13_VIX --> T13_IN
        T13_IN --> T13_FEAT
        T13_FEAT --> T13_MODEL
        T13_MODEL --> T13_OUT
    end
    
    style TILE13 fill:#f59e0b,color:#000
```

```mermaid
graph TB
    subgraph TILE14["Tile 14: Momentum Pulse 💓"]
        T14_IN["📥 INPUTS"]
        T14_NIFTY["NIFTY Spot (Live)"]
        T14_HIST["NIFTY OHLCV (1 Year)"]
        T14_VIX["India VIX"]
        T14_FEAT["Features: RSI, MACD, returns,<br/>volatility, VIX percentile"]
        T14_MODEL1["🧠 XGBoost Momentum"]
        T14_MODEL2["🧠 GBM Divergence"]
        T14_OUT["📤 OUTPUT: Momentum Score 0-100<br/>+ Divergence Detection"]
        
        T14_NIFTY --> T14_IN
        T14_HIST --> T14_IN
        T14_VIX --> T14_IN
        T14_IN --> T14_FEAT
        T14_FEAT --> T14_MODEL1
        T14_FEAT --> T14_MODEL2
        T14_MODEL1 --> T14_OUT
        T14_MODEL2 --> T14_OUT
    end
    
    style TILE14 fill:#8b5cf6,color:#fff
```

---

#### 🔵 **STATISTICAL/FORMULA TILES (16 Tiles)**

| Tile | Exact Input Combination | Formula/Method | Output |
|------|------------------------|----------------|--------|
| **1. Spot Price** | Direct Feed | `yfinance.fast_info` | Real-time Price |
| **2. India VIX** | Direct Feed | `yfinance.fast_info` | Real-time Volatility |
| **3. Probability Surface** | NIFTY Spot + VIX (as σ) | `merton_jump_diffusion(spot, vix/100, T=5)` | 3D probability heatmap |
| **5. Kelly Optimal** | NIFTY Historical Returns | `(p*b - q) / b` where p=win_rate, q=1-p, b=avg_win/avg_loss | Position size % |
| **6. VaR Gauge** | NIFTY 1-year Returns | `np.percentile(returns, [5, 1])` | 95%, 99% VaR |
| **7. Hurst Compass** | NIFTY Close Prices | `rescaled_range_analysis(close, 200)` | Hurst Exponent 0-1 |
| **8. VIX Term Contour** | VIX only | `(vix_20d_avg - vix_5d_avg) / vix_20d_avg` | Contango/Backwardation |
| **9. Friday Fear** | NIFTY Fri Close, Mon Open | `np.percentile(abs(gaps), [50,75,90])` | Gap percentiles |
| **10. Theta Decay** | NIFTY Spot + VIX | `black_scholes_theta(S, K, T, r, sigma)` | Decay curve |
| **11. Monte Carlo Cones**| NIFTY Spot + VIX | `np.percentile(simulated_paths, [16,50,84])` | 1σ, 2σ, 3σ cones |
| **12. Barrier Breach** | NIFTY Spot + VIX + Strike | `prob_touch_barrier(spot, barrier, sigma, T)` | Touch probability |
| **14. Pain Zone** | NIFTY Close + Volume | `np.average(prices, weights=volumes)` | Volume-weighted center |
| **17. GEX Cluster** | NIFTY Volume | `volume_change * 0.1` (proxy only) | Estimated GEX |
| **18. Event Radar** | Calendar + NIFTY History | Lookup table of event impacts | Upcoming events |
| **19. Trade Traffic** | Regime + VIX + Momentum | `IF Trending AND VIX<20 AND Mom>60 THEN GREEN` | GO/WAIT/STOP Signal |
| **20. FOMO Meter** | RSI + Bollinger | `Mean Reversion Logic` | Overbought/Oversold Gauge |

---

### Data Source Summary

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    DATA SOURCES BY TILE                                     │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  NIFTY SPOT PRICE (Live, every 30 min)                                      │
│  ════════════════════════════════════                                       │
│  Used by: ALL 16 TILES                                                      │
│  Source: yfinance.Ticker("^NSEI").fast_info                                │
│                                                                             │
│  NIFTY OHLCV HISTORY (1 Year, cached)                                       │
│  ═══════════════════════════════════                                        │
│  Used by: ALL 16 TILES                                                      │
│  Source: yfinance.download("^NSEI", period="1y")                           │
│  Purpose: Calculate RSI, MACD, Bollinger, Returns, Volatility              │
│                                                                             │
│  INDIA VIX (Live + Historical)                                              │
│  ═════════════════════════════                                              │
│  Used by: 10 TILES (1, 2, 6, 8, 9, 10, 11, 13, 14, and implied vol tiles)  │
│  Source: yfinance.download("^INDIAVIX")                                    │
│  Purpose: Volatility input for Black-Scholes, VIX percentile, term struct │
│                                                                             │
│  BANKNIFTY DATA                                                             │
│  ═══════════════                                                            │
│  Used by: OPTIONAL (if user selects BANKNIFTY view)                        │
│  Note: Dashboard defaults to NIFTY, can switch to BANKNIFTY                │
│  All formulas apply same way to BANKNIFTY                                  │
│                                                                             │
│  ML TRAINED MODELS (.pkl files)                                             │
│  ══════════════════════════════                                             │
│  Used by: 4 TILES (2, 11, 13, 14)                                          │
│  Source: Weekly training on 20 years of NIFTY + VIX data                   │
│  Stored: models/hmm_regime.pkl, rf_reversal.pkl, qr_range.pkl, etc.       │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

---

### Visual: ML Tiles vs Non-ML Tiles

```
                    20 TILES IN OMEGA VAULT
    ┌───────────────────────────────────────────────────────┐
    │                                                        │
    │   🧠 ML-POWERED (4 tiles)     │   📊 STATISTICAL (16)  │
    │   ═════════════════════       │   ═══════════════════  │
    │                               │                        │
    │   ┌──────────────────┐        │   ┌──────────────────┐ │
    │   │ 4. Regime Beacon │        │   │ 1. Spot Price    │ │
    │   │    (HMM)         │        │   │ 2. India VIX     │ │
    │   └──────────────────┘        │   │ 3. Prob Surface  │ │
    │                               │   │ 5. Kelly Optimal │ │
    │   ┌──────────────────┐        │   │ 6. VaR Gauge     │ │
    │   │ 13. Streak       │        │   │ 7. Hurst Compass │ │
    │   │     Reversal     │        │   │ 8. VIX Term      │ │
    │   │     (RF)         │        │   │ 9. Friday Fear   │ │
    │   └──────────────────┘        │   │ 10. Theta Decay  │ │
    │                               │   │ 11. MC Cones     │ │
    │   ┌──────────────────┐        │   │ 12. Barrier      │ │
    │   │ 15. Range        │        │   │ 14. Pain Zone    │ │
    │   │     Quartiles    │        │   │ 17. GEX Cluster  │ │
    │   │     (QR)         │        │   │ 18. Event Radar  │ │
    │   └──────────────────┘        │   │ 19. Traffic Light│ │
    │                               │   │ 20. FOMO Meter   │ │
    │   ┌──────────────────┐        │   └──────────────────┘ │
    │   │ 16. Momentum     │        │                        │
    │   │     Pulse        │        │                        │
    │   │     (XGB+GBM)    │        │                        │
    │   └──────────────────┘        │                        │
    │                               │                        │
    └───────────────────────────────────────────────────────┘
    
    ML tiles use: NIFTY Spot + NIFTY History + VIX + Trained Brain (.pkl)
    Statistical tiles use: NIFTY Spot + NIFTY History + VIX (formulas only)
```

---

## 📊 The Problem We Solve

| Problem | Competition | Omega Vault Solution |
|---------|-------------|---------------------|
| Traders rely on **gut feeling** | Basic candlestick charts | **Bayesian probability signals** with confidence intervals |
| No understanding of **expected value** | "Buy/Sell" alerts | **Kelly Criterion position sizing** with bankroll optimization |
| Ignoring **regime changes** | Static indicators | **Hidden Markov Model regime detection** updated every 30 min |
| Fear of **VIX spikes** | Simple VIX number | **VIX Term Structure analysis** with contango/backwardation signals |
| Options **theta decay** blindness | Premium calculators | **Optimal DTE heatmaps** with decay acceleration curves |
| **Weekend gap risk** ignorance | No gap analysis | **Friday Close Risk Index** with historical gap distributions |

---

## 🏆 Zero Competition Moat

### What Makes This Unique?

1. **Probability-First Design**: Every tile shows probabilities, not just signals
2. **Options-Specific Intelligence**: Designed for F&O traders, not equity investors
3. **Institutional Formulas Made Accessible**: Complex math → simple visual tiles
4. **NIFTY/BANKNIFTY Focus**: Not diluted across 500 stocks
5. **Free Forever**: Ad-supported, no premium paywalls
6. **SEBI Compliant**: No recommendations, only statistical analysis

### Target Audience

- **Option Buyers**: Looking for high-probability breakout entries
- **Option Sellers**: Seeking low-volatility premium collection windows
- **Straddle/Strangle Traders**: Needing volatility regime clarity
- **Weekly Expiry Traders**: Requiring gamma/theta decay timing
- **Position Sizing Beginners**: Learning bankroll management

---

## 🧠 Core Intelligence Engines

### 1. **The Probability Oracle** (Primary Engine)
Generates probability distributions for next-day price movements using:
- **Bayesian Updating**: Prior beliefs + new OHLCV evidence
- **Monte Carlo Simulations**: 10,000 path simulations per run
- **Jump-Diffusion Models** (Merton): Accounts for sudden gaps

### 2. **The Regime Sentinel** (Market State Engine)
Detects and classifies market regimes:
- **Hidden Markov Models (HMM)**: 3-state regime (Trending/Mean-Reverting/Chaotic)
- **Markov Switching GARCH**: Volatility regime transitions
- **Structural Break Detection**: Identifies regime shift events

### 3. **The Risk Architect** (Position Sizing Engine)
Optimizes trade sizing using:
- **Kelly Criterion**: Optimal fraction of bankroll per trade
- **Fractional Kelly (1/4 Kelly)**: Conservative risk management
- **Value at Risk (VaR)**: 95% and 99% confidence loss bounds
---

## 🏗️ System Architecture (Mermaid Diagrams)

### 1. High-Level System Architecture

```mermaid
graph TB
    subgraph USER["👤 USER"]
        BROWSER["🌐 Browser<br/>Desktop / Mobile"]
    end
    
    subgraph FRONTEND["⚛️ FRONTEND (Vite + React)"]
        REACT["React 18<br/>TypeScript"]
        TILES["16 Tile Components"]
        CHARTS["Recharts<br/>Visualizations"]
        THEME["TRON Legacy<br/>Theme"]
    end
    
    subgraph CDN["☁️ CLOUDFLARE PAGES"]
        STATIC["Static Files<br/>HTML/CSS/JS"]
        JSON_DATA["omega_vault.json<br/>Predictions Data"]
    end
    
    subgraph GITHUB["🔧 GITHUB"]
        REPO["Repository<br/>Source Code"]
        ACTIONS["GitHub Actions<br/>CI/CD"]
        MODELS["models/*.pkl<br/>THE BRAIN"]
    end
    
    subgraph PYTHON["🐍 PYTHON ENGINE"]
        TRAIN["train_all_models.py<br/>Weekly Training"]
        INFER["infer.py<br/>Daily Inference"]
        FEATURES["feature_builder.py<br/>60+ Features"]
    end
    
    subgraph YFINANCE["📊 YFINANCE API"]
        NIFTY["^NSEI<br/>NIFTY 50"]
        BANK["^NSEBANK<br/>BANKNIFTY"]
        VIX["^INDIAVIX<br/>India VIX"]
    end
    
    USER --> BROWSER
    BROWSER --> CDN
    CDN --> STATIC
    CDN --> JSON_DATA
    
    ACTIONS --> TRAIN
    ACTIONS --> INFER
    TRAIN --> MODELS
    MODELS --> INFER
    
    YFINANCE --> TRAIN
    YFINANCE --> INFER
    INFER --> JSON_DATA
    
    REPO --> ACTIONS
    
    REACT --> TILES
    TILES --> CHARTS
    CHARTS --> THEME
    
    style USER fill:#4c1d95,color:#fff
    style FRONTEND fill:#3b82f6,color:#fff
    style CDN fill:#f59e0b,color:#000
    style GITHUB fill:#1f2937,color:#fff
    style PYTHON fill:#10b981,color:#fff
    style YFINANCE fill:#ef4444,color:#fff
```

---

### 2. Complete Data Pipeline Flow

```mermaid
flowchart TB
    subgraph SOURCES["📊 DATA SOURCES"]
        YF["yfinance API"]
        NIFTY_D["NIFTY OHLCV<br/>2005 → Present"]
        BANK_D["BANKNIFTY OHLCV<br/>2005 → Present"]
        VIX_D["India VIX<br/>2008 → Present"]
    end
    
    subgraph STORAGE["💾 DATA STORAGE"]
        CSV["Local CSV Cache<br/>data/*.csv"]
        PKL["Model Files<br/>models/*.pkl"]
    end
    
    subgraph PROCESSING["🔧 PROCESSING"]
        FETCH["data_fetcher.py<br/>Download Data"]
        CLEAN["Data Cleaning<br/>Handle Missing Values"]
        ENGINEER["feature_builder.py<br/>60+ Technical Features"]
    end
    
    subgraph TRAINING["🧠 MODEL TRAINING"]
        HMM["HMM Regime<br/>hmmlearn"]
        RF["Random Forest<br/>sklearn"]
        XGB["XGBoost<br/>Gradient Boosting"]
        QR["Quantile Regression<br/>sklearn"]
        GBM["GBM Divergence<br/>sklearn"]
    end
    
    subgraph INFERENCE["⚡ INFERENCE"]
        LOAD["Load .pkl Models"]
        LIVE["Fetch Live Prices"]
        MIX["Mix Features + Brain"]
        PREDICT["Generate Predictions"]
    end
    
    subgraph OUTPUT["📤 OUTPUT"]
        JSON["omega_vault.json"]
        DASH["Dashboard<br/>16 Tiles"]
    end
    
    YF --> NIFTY_D & BANK_D & VIX_D
    NIFTY_D & BANK_D & VIX_D --> FETCH
    FETCH --> CSV
    CSV --> CLEAN
    CLEAN --> ENGINEER
    
    ENGINEER --> HMM & RF & XGB & QR & GBM
    HMM & RF & XGB & QR & GBM --> PKL
    
    PKL --> LOAD
    YF --> LIVE
    LOAD & LIVE --> MIX
    MIX --> PREDICT
    PREDICT --> JSON
    JSON --> DASH
    
    style SOURCES fill:#ef4444,color:#fff
    style PROCESSING fill:#f59e0b,color:#000
    style TRAINING fill:#10b981,color:#fff
    style INFERENCE fill:#3b82f6,color:#fff
    style OUTPUT fill:#8b5cf6,color:#fff
```

---

### 3. GitHub Actions CI/CD Workflow

```mermaid
flowchart LR
    subgraph TRIGGERS["🎯 TRIGGERS"]
        CRON_SAT["⏰ Cron<br/>Saturday 00:00 UTC"]
        CRON_30["⏰ Cron<br/>Every 30 min M-F"]
        MANUAL["🖱️ Manual<br/>workflow_dispatch"]
    end
    
    subgraph WEEKLY["📅 WEEKLY TRAINING"]
        W1["Checkout Repo"]
        W2["Setup Python 3.12"]
        W3["Install Dependencies"]
        W4["Run train_all_models.py"]
        W5["Commit models/*.pkl"]
        W6["Push to main"]
    end
    
    subgraph DAILY["⚡ DAILY INFERENCE"]
        D1["Checkout Repo"]
        D2["Setup Python 3.12"]
        D3["Install Dependencies"]
        D4["Run infer.py"]
        D5["Commit omega_vault.json"]
        D6["Push to main"]
    end
    
    subgraph DEPLOY["🚀 DEPLOY"]
        CF["Cloudflare Pages<br/>Auto-deploy on push"]
        LIVE["Live Dashboard<br/>Updated"]
    end
    
    CRON_SAT --> W1
    MANUAL --> W1
    W1 --> W2 --> W3 --> W4 --> W5 --> W6
    
    CRON_30 --> D1
    D1 --> D2 --> D3 --> D4 --> D5 --> D6
    
    W6 --> CF
    D6 --> CF
    CF --> LIVE
    
    style TRIGGERS fill:#f59e0b,color:#000
    style WEEKLY fill:#10b981,color:#fff
    style DAILY fill:#3b82f6,color:#fff
    style DEPLOY fill:#8b5cf6,color:#fff
```

---

### 4. Frontend-Backend Interaction

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant B as 🌐 Browser
    participant CF as ☁️ Cloudflare
    participant GH as 🔧 GitHub Actions
    participant PY as 🐍 Python Engine
    participant YF as 📊 yfinance
    
    Note over GH,YF: Every 30 min during market hours
    
    GH->>PY: Run infer.py
    PY->>YF: fetch("^NSEI", "^NSEBANK", "^INDIAVIX")
    YF-->>PY: OHLCV + Live Prices
    PY->>PY: Build features (60+)
    PY->>PY: Load models/*.pkl (THE BRAIN)
    PY->>PY: Run predictions
    PY->>GH: Generate omega_vault.json
    GH->>CF: git push (triggers deploy)
    CF->>CF: Rebuild & Deploy
    
    Note over U,B: User opens dashboard
    
    U->>B: Open omega-vault.com
    B->>CF: GET /
    CF-->>B: index.html + JS bundle
    B->>CF: GET /data/omega_vault.json
    CF-->>B: Predictions JSON
    B->>B: Render 16 tiles
    B-->>U: Display dashboard
    
    Note over B: Auto-refresh every 5 min
    
    B->>CF: GET /data/omega_vault.json
    CF-->>B: Updated predictions
    B->>B: Re-render tiles
    B-->>U: Updated display
```

---

### 5. Model Training Deep Dive

```mermaid
flowchart TB
    subgraph INPUT["📥 INPUT DATA"]
        RAW["20 Years OHLCV<br/>~5,000 Trading Days"]
    end
    
    subgraph FEATURES["🔧 FEATURE ENGINEERING"]
        direction TB
        F1["Price Features<br/>Returns, Log Returns"]
        F2["Volatility Features<br/>10d, 20d, 60d Rolling"]
        F3["Technical Indicators<br/>RSI, MACD, BB, ATR"]
        F4["VIX Features<br/>Level, Percentile, Term"]
        F5["Volume Features<br/>Ratio, Change"]
        F6["Streak Features<br/>Consecutive Up/Down"]
    end
    
    subgraph LABELS["🏷️ LABEL GENERATION"]
        direction TB
        L1["Reversal Label<br/>Did streak reverse?"]
        L2["Momentum Label<br/>Was there 1.5%+ move?"]
        L3["Range Label<br/>What was next-day range?"]
        L4["Regime Label<br/>HMM assigns states"]
    end
    
    subgraph SPLIT["✂️ TRAIN/TEST SPLIT"]
        TRAIN_SET["Training Set<br/>80% (~4,000 days)"]
        TEST_SET["Test Set<br/>20% (~1,000 days)"]
    end
    
    subgraph ALGORITHMS["🧠 ML ALGORITHMS"]
        direction TB
        ALG1["HMM<br/>Expectation-Maximization"]
        ALG2["Random Forest<br/>200 Trees, Gini Split"]
        ALG3["XGBoost<br/>Gradient Boosting"]
        ALG4["Quantile Regression<br/>Q10, Q25, Q50, Q75, Q90"]
        ALG5["Gradient Boosting<br/>100 Trees"]
    end
    
    subgraph OPTIMIZATION["⚙️ OPTIMIZATION"]
        OPT1["Minimize Error<br/>Cross-Entropy Loss"]
        OPT2["Find Best Splits<br/>Gini Impurity"]
        OPT3["Iteratively Reduce<br/>Residual Errors"]
    end
    
    subgraph OUTPUT["💾 OUTPUT"]
        PKL1["hmm_regime.pkl"]
        PKL2["rf_reversal.pkl"]
        PKL3["xgb_momentum.pkl"]
        PKL4["qr_range.pkl"]
        PKL5["gbm_divergence.pkl"]
    end
    
    RAW --> FEATURES
    F1 & F2 & F3 & F4 & F5 & F6 --> LABELS
    LABELS --> SPLIT
    SPLIT --> TRAIN_SET & TEST_SET
    TRAIN_SET --> ALGORITHMS
    ALGORITHMS --> OPTIMIZATION
    OPTIMIZATION --> OUTPUT
    
    style INPUT fill:#ef4444,color:#fff
    style FEATURES fill:#f59e0b,color:#000
    style LABELS fill:#84cc16,color:#000
    style ALGORITHMS fill:#10b981,color:#fff
    style OUTPUT fill:#3b82f6,color:#fff
```

---

### 6. Dashboard Rendering Flow

```mermaid
flowchart TB
    subgraph FETCH["📡 DATA FETCHING"]
        REACT_QUERY["React Query<br/>useQuery()"]
        JSON_FETCH["Fetch omega_vault.json"]
        CACHE["5-min Cache<br/>Stale-while-revalidate"]
    end
    
    subgraph PARSE["🔍 DATA PARSING"]
        VALIDATE["Zod Schema<br/>Validation"]
        TRANSFORM["Transform to<br/>Tile Props"]
    end
    
    subgraph TILES["🎨 TILE RENDERING"]
        direction LR
        T1["Tile 1<br/>Probability"]
        T2["Tile 2<br/>Regime"]
        T3["Tile 3<br/>Kelly"]
        T4["Tile 4<br/>VaR"]
        T5["..."]
        T16["Tile 16<br/>Events"]
    end
    
    subgraph CHARTS["📊 CHART COMPONENTS"]
        RECHARTS["Recharts Library"]
        LINE["Line Charts"]
        BAR["Bar Charts"]
        GAUGE["Gauge Dials"]
        HEATMAP["Heatmaps"]
    end
    
    subgraph STYLING["🎨 STYLING"]
        TAILWIND["Tailwind CSS"]
        FRAMER["Framer Motion<br/>Animations"]
        TRON["TRON Theme<br/>Cyan Glow"]
    end
    
    subgraph DISPLAY["🖥️ DISPLAY"]
        GRID["4x4 Grid Layout"]
        HERO["Verdict Hero Section"]
        RESPONSIVE["Responsive<br/>Mobile/Desktop"]
    end
    
    REACT_QUERY --> JSON_FETCH
    JSON_FETCH --> CACHE
    CACHE --> VALIDATE
    VALIDATE --> TRANSFORM
    TRANSFORM --> TILES
    
    T1 & T2 & T3 & T4 & T5 & T16 --> CHARTS
    CHARTS --> RECHARTS
    RECHARTS --> LINE & BAR & GAUGE & HEATMAP
    
    TILES --> STYLING
    TAILWIND & FRAMER & TRON --> DISPLAY
    GRID & HERO --> RESPONSIVE
    
    style FETCH fill:#3b82f6,color:#fff
    style PARSE fill:#f59e0b,color:#000
    style TILES fill:#10b981,color:#fff
    style CHARTS fill:#8b5cf6,color:#fff
    style DISPLAY fill:#ec4899,color:#fff
```

---

### 7. Complete End-to-End Flow

```mermaid
graph TB
    subgraph WEEK["📅 WEEKLY (Saturday)"]
        W1["🌐 yfinance<br/>Download 20 Years"]
        W2["🔧 Build 60+ Features"]
        W3["🧠 Train 5 Models"]
        W4["💾 Save .pkl Files"]
        W5["📤 Commit to GitHub"]
    end
    
    subgraph DAY["⚡ EVERY 30 MIN (M-F)"]
        D1["🌐 yfinance<br/>Fetch Live Prices"]
        D2["📂 Load .pkl Models"]
        D3["🔧 Build Today's Features"]
        D4["🔄 Mix Features + Brain"]
        D5["📊 Generate Predictions"]
        D6["📤 Save omega_vault.json"]
        D7["🚀 Deploy to Cloudflare"]
    end
    
    subgraph USER["👤 USER REQUEST"]
        U1["🌐 Open Browser"]
        U2["📡 Fetch JSON"]
        U3["🎨 Render 16 Tiles"]
        U4["✨ Display Dashboard"]
    end
    
    W1 --> W2 --> W3 --> W4 --> W5
    W5 -.->|"Models ready"| D2
    
    D1 --> D3
    D2 --> D4
    D3 --> D4
    D4 --> D5 --> D6 --> D7
    
    D7 -.->|"Data ready"| U2
    U1 --> U2 --> U3 --> U4
    
    style WEEK fill:#f59e0b,color:#000
    style DAY fill:#10b981,color:#fff
    style USER fill:#3b82f6,color:#fff
```

---

### 8. Technology Stack Diagram

```mermaid
graph LR
    subgraph FRONTEND["⚛️ Frontend Stack"]
        VITE["Vite 5.4"]
        REACT["React 18"]
        TS["TypeScript 5.3"]
        TW["Tailwind CSS 3.4"]
        FM["Framer Motion 11"]
        RC["Recharts 2.15"]
        RQ["React Query 5"]
    end
    
    subgraph BACKEND["🐍 Backend Stack"]
        PY["Python 3.12"]
        YF["yfinance 0.2"]
        PD["Pandas 2.2"]
        NP["NumPy 1.26"]
        SK["scikit-learn 1.4"]
        XG["XGBoost 2.0"]
        HMM["hmmlearn 0.3"]
        JB["Joblib 1.4"]
    end
    
    subgraph INFRA["☁️ Infrastructure"]
        GH["GitHub<br/>Repository"]
        GA["GitHub Actions<br/>CI/CD"]
        CF["Cloudflare Pages<br/>Hosting"]
    end
    
    VITE --> REACT
    REACT --> TS
    TS --> TW
    TW --> FM
    FM --> RC
    RC --> RQ
    
    PY --> YF
    YF --> PD
    PD --> NP
    NP --> SK
    SK --> XG
    XG --> HMM
    HMM --> JB
    
    GH --> GA
    GA --> CF
    
    style FRONTEND fill:#3b82f6,color:#fff
    style BACKEND fill:#10b981,color:#fff
    style INFRA fill:#f59e0b,color:#000
```

---

### 9. Inference Decision Flow

```mermaid
flowchart TD
    START([Start Inference])
    
    FETCH["Fetch Live Data<br/>NIFTY, BANKNIFTY, VIX"]
    CHECK{"Data Available?"}
    
    FALLBACK["Use Cached Data<br/>Last Known Prices"]
    BUILD["Build Features<br/>60+ Indicators"]
    
    LOAD["Load Models<br/>5 .pkl Files"]
    CHECK_MODELS{"Models Exist?"}
    
    ERROR["Return Error<br/>Models Not Trained"]
    
    REGIME["HMM: Predict Regime<br/>TRENDING / REVERTING / CHAOTIC"]
    REVERSAL["RF: Predict Reversal<br/>Probability 0-100%"]
    MOMENTUM["XGB: Predict Momentum<br/>Score 0-100"]
    RANGE["QR: Predict Range<br/>Q10, Q25, Q50, Q75, Q90"]
    DIVERGENCE["GBM: Detect Divergence<br/>Bullish / Bearish"]
    
    COMBINE["Combine Predictions<br/>Build JSON Object"]
    VaR["Calculate VaR<br/>95%, 99% Bounds"]
    KELLY["Calculate Kelly<br/>Position Size"]
    
    SAVE["Save omega_vault.json"]
    DEPLOY["Trigger Cloudflare Deploy"]
    
    FINISH([End Inference])
    
    START --> FETCH
    FETCH --> CHECK
    CHECK -->|Yes| BUILD
    CHECK -->|No| FALLBACK
    FALLBACK --> BUILD
    
    BUILD --> LOAD
    LOAD --> CHECK_MODELS
    CHECK_MODELS -->|Yes| REGIME
    CHECK_MODELS -->|No| ERROR
    
    REGIME --> REVERSAL
    REVERSAL --> MOMENTUM
    MOMENTUM --> RANGE
    RANGE --> DIVERGENCE
    
    DIVERGENCE --> COMBINE
    COMBINE --> VaR
    VaR --> KELLY
    KELLY --> SAVE
    SAVE --> DEPLOY
    DEPLOY --> FINISH
    
    style START fill:#10b981,color:#fff
    style FINISH fill:#3b82f6,color:#fff
    style ERROR fill:#ef4444,color:#fff
```

---

### 10. User Journey Flow

```mermaid
journey
    title User Journey: From Landing to Trading Decision
    section Landing
      Open Website: 5: User
      See TRON Theme: 5: User
      View Verdict Hero: 5: User
    section Understanding
      Read Market Regime: 4: User
      Check Probability Surface: 4: User
      Review VaR Gauge: 4: User
    section Analysis
      Study Momentum Pulse: 3: User
      Check Streak Reversal: 3: User
      View Range Quartiles: 4: User
    section Decision
      Note Kelly Size: 5: User
      Set Position Size: 5: User
      Execute Trade: 5: User
    section Return
      Bookmark PWA: 5: User
      Return Every 30 min: 5: User
```

---

## 🤖 Machine Learning Models - Complete Specification

### ✅ Your Understanding is 100% CORRECT!

Yes, this is EXACTLY what happens. Let me confirm with a clear diagram:

```mermaid
graph TB
    subgraph WEEKLY["📅 WEEKLY: Build The Brain (Saturdays)"]
        direction TB
        A1["📥 Download 20 Years Data<br/>NIFTY, BANKNIFTY, VIX<br/>from yfinance (2005 → Now)"] 
        A2["🔧 Build 60+ Features<br/>RSI, MACD, Bollinger, VIX, etc."]
        A3["🧠 Train 5 ML Models<br/>HMM, RandomForest, XGBoost, etc."]
        A4["💾 Save as .pkl files<br/>THE BRAIN<br/>(~9.4 MB)"]
        
        A1 --> A2 --> A3 --> A4
    end
    
    subgraph DAILY["⚡ EVERY 30 MIN: Use The Brain (Market Hours)"]
        direction TB
        B1["📡 Fetch LIVE Prices<br/>NIFTY spot, BANKNIFTY spot, VIX<br/>from yfinance"]
        B2["📂 Load The Brain<br/>(pre-trained .pkl models)"]
        B3["🔄 Mix Live + Brain<br/>Build features from live data<br/>Feed to trained models"]
        B4["📊 Generate Predictions<br/>Regime, Momentum, Range, etc."]
        B5["🖥️ Display on Dashboard<br/>16 Tiles Updated"]
        
        B1 --> B3
        B2 --> B3
        B3 --> B4 --> B5
    end
    
    A4 -.->|"Brain is ready<br/>waiting to be used"| B2
    
    style A4 fill:#f59e0b,color:#000
    style B3 fill:#10b981,color:#000
    style B5 fill:#3b82f6,color:#fff
```

### 🔄 The Complete Flow (Simple Explanation)

| Step | When | What Happens | Result |
|------|------|--------------|--------|
| **1. Data Collection** | Weekly (Saturday) | Download 20 years of NIFTY, BANKNIFTY, VIX OHLCV data from yfinance | ~5,000 rows of historical data |
| **2. Feature Engineering** | Weekly (Saturday) | Calculate RSI, MACD, Bollinger Bands, volatility, VIX features, etc. | 60+ features per day |
| **3. Model Training** | Weekly (Saturday) | Feed features + labels to ML algorithms | 5 trained models (THE BRAIN) |
| **4. Save Brain** | Weekly (Saturday) | Save trained models as .pkl files | ~9.4 MB of "learned patterns" |
| **5. Load Brain** | Every 30 min (M-F) | Load the pre-trained .pkl models into memory | Brain is ready to predict |
| **6. Fetch Live Prices** | Every 30 min (M-F) | Get today's NIFTY spot, BANKNIFTY spot, VIX from yfinance | Current market state |
| **7. Mix Live + Brain** | Every 30 min (M-F) | Build features from live data, feed to brain | Predictions generated |
| **8. Display Dashboard** | Every 30 min (M-F) | Show predictions in 16 tiles | User sees insights |

---

## 🎓 How Training Actually Works (The Process Behind It)

### What is "Training" in Simple Terms?

**Training = Teaching the model patterns from historical data**

Imagine you want to teach a child to recognize when a market reversal is likely. You would show them thousands of examples:
- "When price went up 5 days in a row AND RSI was above 70, it reversed 65% of the time"
- "When VIX was below 12 AND volatility was low, market trended 70% of the time"

That's exactly what ML training does, but with math instead of words.

### The Training Process (Step-by-Step)

```mermaid
graph TB
    subgraph STEP1["STEP 1: Prepare Raw Data"]
        R1["20 Years OHLCV<br/>Open, High, Low, Close, Volume"]
        R2["~5,000 trading days<br/>for NIFTY, BANKNIFTY, VIX"]
    end
    
    subgraph STEP2["STEP 2: Create Features (X)"]
        F1["Calculate for EACH day:"]
        F2["• RSI = 65.3"]
        F3["• MACD = +12.5"]
        F4["• Volatility = 1.2%"]
        F5["• VIX = 14.2"]
        F6["• 60+ more features..."]
    end
    
    subgraph STEP3["STEP 3: Create Labels (Y)"]
        L1["For EACH day, what happened NEXT?"]
        L2["• Did price reverse? (0 or 1)"]
        L3["• Was there strong momentum? (0 or 1)"]
        L4["• What was the range? (number)"]
    end
    
    subgraph STEP4["STEP 4: Train the Model"]
        T1["Algorithm learns patterns:"]
        T2["IF RSI > 70 AND VIX < 15"]
        T3["THEN reversal probability = 0.65"]
        T4["These patterns stored in .pkl file"]
    end
    
    STEP1 --> STEP2
    STEP2 --> STEP3
    STEP3 --> STEP4
    
    style STEP2 fill:#3b82f6,color:#fff
    style STEP3 fill:#f59e0b,color:#000
    style STEP4 fill:#10b981,color:#fff
```

### Detailed Training Example: Streak Reversal Model

Let me show you EXACTLY how the Random Forest Reversal model learns:

#### Step 1: Create Feature-Label Pairs from Historical Data

```python
# For EACH day in 20 years of data, we create a row like this:

# Day: 2023-07-15
# FEATURES (X) - What we know BEFORE that day ended:
features = {
    'streak': 4,              # 4 consecutive up days
    'rsi_14': 72.3,           # RSI is overbought
    'bb_position': 0.92,       # Price near upper Bollinger
    'volatility_20d': 0.012,   # Low volatility
    'vix': 11.5,               # Low fear
    'volume_ratio': 1.3,       # Higher than usual volume
    # ... 10 total features
}

# LABEL (Y) - What ACTUALLY happened the next day:
label = 1  # The streak DID reverse (price went down on 2023-07-16)

# We do this for ALL 5,000 days!
```

#### Step 2: What the Training Algorithm Does

```python
# When we call model.fit(X, y), the Random Forest does this:

# 1. Creates 200 decision trees
# 2. Each tree looks at random subsets of data
# 3. Each tree learns patterns like:

#    TREE #1:
#    IF streak > 3 AND rsi_14 > 70:
#        IF vix < 12:
#            PREDICT: reversal = 75% likely
#        ELSE:
#            PREDICT: reversal = 55% likely
#    ELSE:
#        PREDICT: reversal = 35% likely

#    TREE #2 (different pattern):
#    IF bb_position > 0.9 AND volatility_20d < 0.015:
#        PREDICT: reversal = 68% likely
#    ...

# 3. All 200 trees vote together for final prediction
```

#### Step 3: How the Model "Learns" (The Math)

```python
# Training is an OPTIMIZATION process
# The model tries to MINIMIZE prediction errors

# For Random Forest:
# 1. Start with all 5,000 samples
# 2. Find the best "split" that separates reversals from non-reversals
#    Example: "IF streak > 3, split here"
# 3. Measure how well the split separates the data (Gini impurity)
# 4. Repeat recursively for each branch
# 5. Do this 200 times with random subsets → 200 trees

# For XGBoost (Momentum model):
# 1. Start with a simple prediction (e.g., 50% momentum)
# 2. Calculate ERROR for each sample
# 3. Build a tree to PREDICT THE ERRORS
# 4. Add this tree to the model, reducing errors
# 5. Repeat 200 times → each tree fixes previous errors

# For HMM (Regime model):
# 1. Assume there are 3 hidden states (regimes)
# 2. Use Expectation-Maximization (EM) algorithm
# 3. E-step: Estimate which regime each day belongs to
# 4. M-step: Update regime parameters (mean return, volatility)
# 5. Repeat until convergence
```

#### Step 4: What Gets Saved in the .pkl File (THE BRAIN)

```python
# After training, the .pkl file contains:

rf_reversal.pkl = {
    'model': RandomForestClassifier(
        # 200 decision trees with learned patterns
        n_estimators=200,
        
        # Each tree contains:
        # - Split rules: "IF streak > 3 THEN go left"
        # - Leaf values: "This leaf predicts 72% reversal"
        
        # Feature importances (what matters most):
        feature_importances_ = [
            ('streak', 0.23),        # Streak is most important
            ('rsi_14', 0.18),        # RSI is second
            ('bb_position', 0.15),   # Bollinger position third
            # ...
        ]
    ),
    'feature_cols': ['streak', 'rsi_14', 'bb_position', ...]
}

# This is "THE BRAIN" - learned patterns from 20 years of data
```

### Training vs Inference (Side by Side)

| Aspect | TRAINING (Weekly) | INFERENCE (Every 30 min) |
|--------|-------------------|--------------------------|
| **When** | Saturday 00:00 UTC | M-F 9:15 AM - 3:30 PM IST |
| **Data Used** | 20 years of history | Last 1 year + live prices |
| **What Happens** | Model LEARNS patterns | Model USES learned patterns |
| **Input** | 5,000 days of features + labels | 1 day of features (today) |
| **Output** | Trained .pkl files (brain) | Predictions (JSON) |
| **CPU/Memory** | High (10-15 min, 2GB RAM) | Low (30 sec, 300MB RAM) |
| **Changes Model?** | Yes (updates weights) | No (read-only) |

### Visual: How Live Prices Mix with The Brain

```
  ┌─────────────────────────────────────────────────────────────┐
  │                    EVERY 30 MINUTES                         │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  📡 FETCH LIVE PRICES                                       │
  │  ┌─────────────────────────────────────────┐                │
  │  │ NIFTY Spot:     24,850.75              │                │
  │  │ BANKNIFTY Spot: 52,340.20              │                │
  │  │ India VIX:      12.35                   │                │
  │  │ (fetched via yfinance.Ticker.fast_info) │                │
  │  └─────────────────────────────────────────┘                │
  │                         │                                   │
  │                         ▼                                   │
  │  🔧 BUILD LIVE FEATURES                                     │
  │  ┌─────────────────────────────────────────┐                │
  │  │ • Combine with last 1 year of data     │                │
  │  │ • Calculate RSI, MACD, BB, etc.        │                │
  │  │ • Calculate volatility, VIX features   │                │
  │  │ • Result: 60+ features for TODAY       │                │
  │  └─────────────────────────────────────────┘                │
  │                         │                                   │
  │                         ▼                                   │
  │  🧠 LOAD THE BRAIN (Pre-trained Models)                     │
  │  ┌─────────────────────────────────────────┐                │
  │  │ hmm_regime.pkl    → Regime patterns    │                │
  │  │ rf_reversal.pkl   → Reversal patterns  │                │
  │  │ xgb_momentum.pkl  → Momentum patterns  │                │
  │  │ qr_range.pkl      → Range patterns     │                │
  │  │ gbm_divergence.pkl→ Divergence patterns│                │
  │  └─────────────────────────────────────────┘                │
  │                         │                                   │
  │                         ▼                                   │
  │  🔄 MIX: Feed Today's Features to Brain                     │
  │  ┌─────────────────────────────────────────┐                │
  │  │ today_features = [rsi=68, macd=+15,    │                │
  │  │                   vix=12.35, streak=2, │                │
  │  │                   volatility=0.011...] │                │
  │  │                                         │                │
  │  │ predictions = brain.predict(today)      │                │
  │  │                                         │                │
  │  │ # Brain says:                           │                │
  │  │ # "I've seen this pattern before..."    │                │
  │  │ # "RSI=68 + VIX=12 + streak=2 usually   │                │
  │  │ #  means TRENDING regime with 72% prob" │                │
  │  └─────────────────────────────────────────┘                │
  │                         │                                   │
  │                         ▼                                   │
  │  📊 GENERATE PREDICTIONS                                    │
  │  ┌─────────────────────────────────────────┐                │
  │  │ {                                       │                │
  │  │   "regime": "TRENDING",                 │                │
  │  │   "regime_probability": 0.72,           │                │
  │  │   "reversal_probability": 0.35,         │                │
  │  │   "momentum_score": 68,                 │                │
  │  │   "range_q50": 245.3,                   │                │
  │  │   ...                                   │                │
  │  │ }                                       │                │
  │  └─────────────────────────────────────────┘                │
  │                         │                                   │
  │                         ▼                                   │
  │  🖥️ UPDATE DASHBOARD (16 Tiles)                             │
  │  ┌─────────────────────────────────────────┐                │
  │  │ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │                │
  │  │ │Regime│ │Moment│ │Range │ │VaR   │    │                │
  │  │ │TREND │ │ 68   │ │±245  │ │1.2%  │    │                │
  │  │ └──────┘ └──────┘ └──────┘ └──────┘    │                │
  │  │ ... 12 more tiles ...                   │                │
  │  └─────────────────────────────────────────┘                │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

### Summary: The Complete Picture

```
┌────────────────────────────────────────────────────────────────────┐
│                         THE SYSTEM                                  │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SATURDAY (Once a Week):                                            │
│  ═══════════════════════                                            │
│                                                                     │
│  yfinance ───► 20 Years ───► 60+ Features ───► TRAIN ───► BRAIN    │
│  (NIFTY)       OHLCV Data    per day           5 Models   (.pkl)   │
│  (BANKNIFTY)   (~5000 days)                                         │
│  (VIX)                                                              │
│                                                                     │
│                                    │                                │
│                                    ▼                                │
│                              ┌──────────┐                           │
│                              │  BRAIN   │                           │
│                              │ (9.4 MB) │                           │
│                              │ Stored   │                           │
│                              │ in GitHub│                           │
│                              └──────────┘                           │
│                                    │                                │
│                                    ▼                                │
│  EVERY 30 MIN (Market Hours):                                       │
│  ═════════════════════════════                                      │
│                                                                     │
│  yfinance ───► Live Spot ───► Build Today's ───► MIX WITH ───► JSON│
│  (NIFTY)       Prices         Features (60+)     BRAIN             │
│  (BANKNIFTY)   (current)                                            │
│  (VIX)                                                              │
│                                                        │            │
│                                                        ▼            │
│                                                   ┌──────────┐      │
│                                                   │DASHBOARD │      │
│                                                   │16 Tiles  │      │
│                                                   │Updated   │      │
│                                                   └──────────┘      │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

### ML Model Inventory

| # | Model Name | Algorithm | Purpose | Tile Used In | File Size |
|---|------------|-----------|---------|--------------|-----------|
| 1 | **HMM Regime Detector** | Hidden Markov Model (Gaussian Emissions) | Classify market regime (Trending/Mean-Reverting/Chaotic) | Regime Beacon | ~1.2 MB |
| 2 | **RF Streak Reversal** | Random Forest Classifier | Predict reversal after consecutive up/down days | Streak Reversal | ~2.5 MB |
| 3 | **XGB Momentum Pulse** | XGBoost Gradient Boosting | Score momentum strength (0-100) | Momentum Pulse | ~3.1 MB |
| 4 | **QR Range Predictor** | Quantile Regression (Linear) | Predict Q10/Q25/Q50/Q75/Q90 price ranges | Range Quartiles | ~0.8 MB |
| 5 | **GBM Divergence Detector** | Gradient Boosting Machine | Detect RSI/MACD/Price divergences | Momentum Pulse | ~1.8 MB |

**Total Model Size**: ~9.4 MB (fits easily in GitHub repo)

---

### Training Data Source (yfinance ONLY)

```mermaid
graph TB
    subgraph "yfinance Downloads"
        YF1["yfinance.download('^NSEI')<br/>NIFTY 50 Index"]
        YF2["yfinance.download('^NSEBANK')<br/>BANKNIFTY Index"]
        YF3["yfinance.download('^INDIAVIX')<br/>India VIX"]
    end
    
    subgraph "Data Range"
        DR["2005 → Present<br/>~20 Years<br/>~5,000 Trading Days"]
    end
    
    subgraph "OHLCV Columns"
        O["Open"]
        H["High"]
        L["Low"]
        C["Close"]
        V["Volume"]
    end
    
    YF1 --> DR
    YF2 --> DR
    YF3 --> DR
    DR --> O
    DR --> H
    DR --> L
    DR --> C
    DR --> V
    
    style YF1 fill:#3b82f6
    style YF2 fill:#10b981
    style YF3 fill:#f59e0b
```

### Data Fetching Code

```python
import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_training_data():
    """
    Fetch NIFTY, BANKNIFTY, VIX data from 2005 using yfinance
    This is the SOLE source of truth - no other data sources
    """
    # NIFTY 50 Index
    nifty = yf.download(
        "^NSEI",
        start="2005-01-01",
        end=datetime.now().strftime("%Y-%m-%d"),
        progress=False
    )
    
    # BANKNIFTY Index
    banknifty = yf.download(
        "^NSEBANK",
        start="2005-01-01",
        end=datetime.now().strftime("%Y-%m-%d"),
        progress=False
    )
    
    # India VIX (available from 2008)
    vix = yf.download(
        "^INDIAVIX",
        start="2008-01-01",
        end=datetime.now().strftime("%Y-%m-%d"),
        progress=False
    )
    
    # Save to CSV for caching
    nifty.to_csv("data/NSEI_daily.csv")
    banknifty.to_csv("data/NSEBANK_daily.csv")
    vix.to_csv("data/INDIAVIX_daily.csv")
    
    return nifty, banknifty, vix
```

---

### Training Frequency

| Schedule | Frequency | What Happens | GitHub Actions |
|----------|-----------|--------------|----------------|
| **Weekly Training** | Every **Saturday 00:00 UTC** | Full model retraining on all historical data | `weekly_training.yml` |
| **Daily Inference** | Every **30 min** (M-F 9:15 AM - 3:30 PM IST) | Load trained models, run predictions | `daily_inference.yml` |

```mermaid
graph LR
    subgraph "WEEKLY (Saturdays)"
        W1["Fetch Full History<br/>2005 → Now"] --> W2["Feature Engineering<br/>60+ Features"]
        W2 --> W3["Train 5 Models"]
        W3 --> W4["Save .pkl Files<br/>to models/"]
        W4 --> W5["Commit to GitHub"]
    end
    
    subgraph "DAILY (Every 30min M-F)"
        D1["Load .pkl Models"] --> D2["Fetch Recent 1Y Data"]
        D2 --> D3["Build Live Features"]
        D3 --> D4["Run Inference"]
        D4 --> D5["Generate JSON"]
        D5 --> D6["Deploy Dashboard"]
    end
    
    W5 -.->|"Models Updated Weekly"| D1
    
    style W3 fill:#f59e0b
    style D4 fill:#10b981
```

---

### Feature Engineering Pipeline

All ML models use features derived from **OHLCV + VIX** data:

```python
def build_features(nifty_df: pd.DataFrame, vix_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build 60+ features from raw OHLCV and VIX data
    These features feed into all 5 ML models
    """
    df = nifty_df.copy()
    
    # ═══════════════════════════════════════════════════════════
    # PRICE-BASED FEATURES (from OHLCV)
    # ═══════════════════════════════════════════════════════════
    
    # Daily Returns
    df['return_1d'] = df['Close'].pct_change(1)
    df['return_5d'] = df['Close'].pct_change(5)
    df['return_20d'] = df['Close'].pct_change(20)
    
    # Log Returns (for statistical models)
    df['log_return'] = np.log(df['Close'] / df['Close'].shift(1))
    
    # Volatility (Rolling Std of Returns)
    df['volatility_10d'] = df['return_1d'].rolling(10).std() * np.sqrt(252)
    df['volatility_20d'] = df['return_1d'].rolling(20).std() * np.sqrt(252)
    df['volatility_60d'] = df['return_1d'].rolling(60).std() * np.sqrt(252)
    
    # ═══════════════════════════════════════════════════════════
    # TECHNICAL INDICATORS (from OHLCV)
    # ═══════════════════════════════════════════════════════════
    
    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    df['rsi_14'] = 100 - (100 / (1 + gain / (loss + 1e-10)))
    
    # MACD
    ema_12 = df['Close'].ewm(span=12).mean()
    ema_26 = df['Close'].ewm(span=26).mean()
    df['macd'] = ema_12 - ema_26
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_histogram'] = df['macd'] - df['macd_signal']
    
    # Bollinger Bands
    df['bb_middle'] = df['Close'].rolling(20).mean()
    df['bb_std'] = df['Close'].rolling(20).std()
    df['bb_upper'] = df['bb_middle'] + 2 * df['bb_std']
    df['bb_lower'] = df['bb_middle'] - 2 * df['bb_std']
    df['bb_position'] = (df['Close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'] + 1e-10)
    
    # ATR (Average True Range)
    high_low = df['High'] - df['Low']
    high_close = abs(df['High'] - df['Close'].shift(1))
    low_close = abs(df['Low'] - df['Close'].shift(1))
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['atr_14'] = tr.rolling(14).mean()
    df['atr_pct'] = df['atr_14'] / df['Close']
    
    # Moving Averages
    df['sma_5'] = df['Close'].rolling(5).mean()
    df['sma_20'] = df['Close'].rolling(20).mean()
    df['sma_50'] = df['Close'].rolling(50).mean()
    df['sma_200'] = df['Close'].rolling(200).mean()
    
    # Price vs Moving Averages
    df['price_vs_sma20'] = (df['Close'] - df['sma_20']) / df['sma_20']
    df['price_vs_sma50'] = (df['Close'] - df['sma_50']) / df['sma_50']
    df['price_vs_sma200'] = (df['Close'] - df['sma_200']) / df['sma_200']
    
    # ═══════════════════════════════════════════════════════════
    # STREAK FEATURES (for Reversal Model)
    # ═══════════════════════════════════════════════════════════
    
    # Consecutive up/down days
    df['up_day'] = (df['return_1d'] > 0).astype(int)
    df['down_day'] = (df['return_1d'] < 0).astype(int)
    
    # Streak counter
    df['streak'] = df['up_day'].groupby(
        (df['up_day'] != df['up_day'].shift()).cumsum()
    ).cumsum() - df['down_day'].groupby(
        (df['down_day'] != df['down_day'].shift()).cumsum()
    ).cumsum()
    
    # ═══════════════════════════════════════════════════════════
    # VIX FEATURES (from India VIX)
    # ═══════════════════════════════════════════════════════════
    
    # Merge VIX data
    df['vix'] = vix_df['Close'].reindex(df.index).ffill()
    df['vix_5d_avg'] = df['vix'].rolling(5).mean()
    df['vix_20d_avg'] = df['vix'].rolling(20).mean()
    df['vix_percentile'] = df['vix'].rolling(252).rank(pct=True)
    
    # VIX Term Structure (proxy using short vs long avg)
    df['vix_term_structure'] = (df['vix_20d_avg'] - df['vix_5d_avg']) / (df['vix_20d_avg'] + 1e-10)
    
    # VIX vs Price Relationship
    df['vix_price_corr'] = df['vix'].rolling(20).corr(df['Close'])
    
    # ═══════════════════════════════════════════════════════════
    # VOLUME FEATURES (from OHLCV)
    # ═══════════════════════════════════════════════════════════
    
    df['volume_sma_20'] = df['Volume'].rolling(20).mean()
    df['volume_ratio'] = df['Volume'] / (df['volume_sma_20'] + 1e-10)
    df['volume_change'] = df['Volume'].pct_change()
    
    # Drop NaN rows
    df = df.dropna()
    
    return df
```

---

### Model #1: HMM Regime Detector

**Algorithm**: Hidden Markov Model with Gaussian Emissions  
**Training Frequency**: Weekly (Saturdays)  
**Used In**: Regime Beacon Tile

```python
from hmmlearn import hmm
import numpy as np
import joblib

def train_hmm_regime(features_df: pd.DataFrame):
    """
    Train Hidden Markov Model for market regime detection
    
    States:
        0: TRENDING (low vol, strong direction)
        1: MEAN-REVERTING (medium vol, oscillating)
        2: CHAOTIC (high vol, unpredictable)
    """
    # Use returns and volatility as observations
    observations = features_df[['return_1d', 'volatility_20d']].values
    
    # Initialize HMM with 3 hidden states
    model = hmm.GaussianHMM(
        n_components=3,           # 3 regimes
        covariance_type="full",   # Full covariance matrix
        n_iter=1000,              # Max iterations
        random_state=42,
        verbose=False
    )
    
    # Train on historical data
    model.fit(observations)
    
    # Get state sequence and probabilities
    hidden_states = model.predict(observations)
    state_probs = model.predict_proba(observations)
    
    # Label states based on learned means
    # State with highest volatility mean = CHAOTIC
    # State with lowest volatility mean = TRENDING
    vol_means = [model.means_[i][1] for i in range(3)]
    state_labels = [''] * 3
    state_labels[np.argmax(vol_means)] = 'CHAOTIC'
    state_labels[np.argmin(vol_means)] = 'TRENDING'
    remaining = [i for i in range(3) if state_labels[i] == ''][0]
    state_labels[remaining] = 'MEAN_REVERTING'
    
    # Save model
    joblib.dump({
        'model': model,
        'state_labels': state_labels,
        'scaler_mean': observations.mean(axis=0),
        'scaler_std': observations.std(axis=0)
    }, 'models/hmm_regime.pkl')
    
    print(f"HMM Regime Model trained on {len(observations)} samples")
    return model, state_labels
```

**Inference (Every 30 min)**:
```python
def infer_regime(features_df: pd.DataFrame):
    """Run regime inference using pre-trained HMM"""
    data = joblib.load('models/hmm_regime.pkl')
    model = data['model']
    state_labels = data['state_labels']
    
    # Get latest observation
    latest = features_df[['return_1d', 'volatility_20d']].iloc[-1:].values
    
    # Predict regime
    state = model.predict(latest)[0]
    probs = model.predict_proba(latest)[0]
    
    return {
        'regime': state_labels[state],
        'regime_probability': float(probs[state]),
        'all_probabilities': {
            state_labels[i]: float(probs[i]) for i in range(3)
        }
    }
```

---

### Model #2: Random Forest Streak Reversal

**Algorithm**: Random Forest Classifier  
**Training Frequency**: Weekly (Saturdays)  
**Used In**: Streak Reversal Tile

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def train_rf_reversal(features_df: pd.DataFrame):
    """
    Train Random Forest to predict streak reversal
    
    Target: Will tomorrow reverse the current streak?
    Features: Streak length, RSI, VIX, volatility, etc.
    """
    df = features_df.copy()
    
    # Create target: Did the streak reverse next day?
    df['streak_sign'] = np.sign(df['streak'])
    df['next_return_sign'] = np.sign(df['return_1d'].shift(-1))
    df['reversal'] = (df['streak_sign'] != df['next_return_sign']).astype(int)
    
    # Features for reversal prediction
    feature_cols = [
        'streak', 'rsi_14', 'bb_position', 'macd_histogram',
        'volatility_20d', 'vix', 'vix_percentile',
        'atr_pct', 'volume_ratio', 'price_vs_sma20'
    ]
    
    # Remove last row (no target) and NaNs
    df = df.dropna()
    X = df[feature_cols].iloc[:-1]
    y = df['reversal'].iloc[:-1]
    
    # Train-test split (80/20)
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
    print(f"RF Reversal - Train: {train_acc:.2%}, Test: {test_acc:.2%}")
    
    # Save model
    joblib.dump({
        'model': model,
        'feature_cols': feature_cols
    }, 'models/rf_reversal.pkl')
    
    return model
```

---

### Model #3: XGBoost Momentum Pulse

**Algorithm**: XGBoost Gradient Boosting  
**Training Frequency**: Weekly (Saturdays)  
**Used In**: Momentum Pulse Tile

```python
from xgboost import XGBClassifier
import joblib

def train_xgb_momentum(features_df: pd.DataFrame):
    """
    Train XGBoost to score momentum strength
    
    Target: Strong momentum (>1.5% move) in next 3 days
    Output: Probability score 0-100
    """
    df = features_df.copy()
    
    # Target: Strong directional move in next 3 days
    df['future_3d_return'] = df['Close'].shift(-3) / df['Close'] - 1
    df['strong_momentum'] = (abs(df['future_3d_return']) > 0.015).astype(int)
    
    feature_cols = [
        'rsi_14', 'macd', 'macd_histogram', 'bb_position',
        'return_1d', 'return_5d', 'return_20d',
        'volatility_10d', 'volatility_20d',
        'atr_pct', 'volume_ratio',
        'price_vs_sma20', 'price_vs_sma50',
        'vix', 'vix_percentile', 'vix_term_structure'
    ]
    
    df = df.dropna()
    X = df[feature_cols].iloc[:-3]
    y = df['strong_momentum'].iloc[:-3]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)
    
    test_acc = model.score(X_test, y_test)
    print(f"XGB Momentum - Test Accuracy: {test_acc:.2%}")
    
    joblib.dump({
        'model': model,
        'feature_cols': feature_cols
    }, 'models/xgb_momentum.pkl')
    
    return model
```

---

### Model #4: Quantile Regression Range Predictor

**Algorithm**: Linear Quantile Regression  
**Training Frequency**: Weekly (Saturdays)  
**Used In**: Range Quartiles Tile

```python
from sklearn.linear_model import QuantileRegressor
import joblib

def train_qr_range(features_df: pd.DataFrame):
    """
    Train Quantile Regression for price range prediction
    
    Predicts Q10, Q25, Q50, Q75, Q90 of next-day price range
    """
    df = features_df.copy()
    
    # Target: Next-day range as % of close
    df['next_range'] = (df['High'].shift(-1) - df['Low'].shift(-1)) / df['Close']
    
    feature_cols = [
        'atr_pct', 'volatility_10d', 'volatility_20d',
        'vix', 'vix_percentile', 'volume_ratio',
        'bb_position', 'rsi_14'
    ]
    
    df = df.dropna()
    X = df[feature_cols].iloc[:-1]
    y = df['next_range'].iloc[:-1]
    
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
        print(f"Quantile {q:.0%} model trained")
    
    joblib.dump({
        'models': models,
        'feature_cols': feature_cols
    }, 'models/qr_range.pkl')
    
    return models
```

---

### Model #5: Gradient Boosting Divergence Detector

**Algorithm**: Gradient Boosting Machine  
**Training Frequency**: Weekly (Saturdays)  
**Used In**: Momentum Pulse Tile (sub-component)

```python
from sklearn.ensemble import GradientBoostingClassifier
import joblib

def train_gbm_divergence(features_df: pd.DataFrame):
    """
    Train GBM to detect RSI/MACD divergences
    
    Bullish Divergence: Price makes lower low, RSI makes higher low
    Bearish Divergence: Price makes higher high, RSI makes lower high
    """
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
    
    feature_cols = [
        'rsi_14', 'macd', 'macd_histogram',
        'return_5d', 'return_20d',
        'bb_position', 'volume_ratio'
    ]
    
    df = df.dropna()
    X = df[feature_cols]
    y = df['divergence']
    
    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X, y)
    
    joblib.dump({
        'model': model,
        'feature_cols': feature_cols
    }, 'models/gbm_divergence.pkl')
    
    return model
```

---

### Complete Training Script (train_all_models.py)

```python
#!/usr/bin/env python3
"""
Omega Vault - Weekly Model Training Script
Runs every Saturday via GitHub Actions

Data Source: yfinance (NIFTY, BANKNIFTY, VIX from 2005)
Output: 5 trained models saved to models/
"""

import os
import sys
import yfinance as yf
import pandas as pd
from datetime import datetime

# Import all training functions
from models.hmm_regime import train_hmm_regime
from models.rf_reversal import train_rf_reversal
from models.xgb_momentum import train_xgb_momentum
from models.qr_range import train_qr_range
from models.gbm_divergence import train_gbm_divergence
from features.feature_builder import build_features

def main():
    print("=" * 60)
    print("OMEGA VAULT - WEEKLY MODEL TRAINING")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Step 1: Fetch Historical Data
    print("\n[1/6] Fetching historical data from yfinance...")
    
    nifty = yf.download("^NSEI", start="2005-01-01", progress=True)
    print(f"  NIFTY: {len(nifty)} rows ({nifty.index[0]} to {nifty.index[-1]})")
    
    banknifty = yf.download("^NSEBANK", start="2005-01-01", progress=True)
    print(f"  BANKNIFTY: {len(banknifty)} rows")
    
    vix = yf.download("^INDIAVIX", start="2008-01-01", progress=True)
    print(f"  VIX: {len(vix)} rows")
    
    # Step 2: Build Features
    print("\n[2/6] Building features from OHLCV + VIX data...")
    features_df = build_features(nifty, vix)
    print(f"  Generated {len(features_df.columns)} features")
    print(f"  Training samples: {len(features_df)}")
    
    # Step 3: Train HMM Regime
    print("\n[3/6] Training HMM Regime Detector...")
    train_hmm_regime(features_df)
    
    # Step 4: Train RF Reversal
    print("\n[4/6] Training Random Forest Reversal...")
    train_rf_reversal(features_df)
    
    # Step 5: Train XGB Momentum
    print("\n[5/6] Training XGBoost Momentum...")
    train_xgb_momentum(features_df)
    
    # Step 6: Train QR Range
    print("\n[6/6] Training Quantile Regression Range...")
    train_qr_range(features_df)
    
    # Step 7: Train GBM Divergence
    print("\n[7/7] Training GBM Divergence...")
    train_gbm_divergence(features_df)
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print(f"Models saved to: models/")
    print(f"Finished at: {datetime.now().isoformat()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

---

### Inference Script (infer.py)

```python
#!/usr/bin/env python3
"""
Omega Vault - Daily Inference Script
Runs every 30 min (M-F 9:15 AM - 3:30 PM IST)

Loads pre-trained models, fetches live data, generates predictions
Output: omega_vault.json for dashboard
"""

import os
import json
import joblib
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

from features.feature_builder import build_features

def load_all_models():
    """Load all pre-trained models from models/ directory"""
    models = {
        'hmm_regime': joblib.load('models/hmm_regime.pkl'),
        'rf_reversal': joblib.load('models/rf_reversal.pkl'),
        'xgb_momentum': joblib.load('models/xgb_momentum.pkl'),
        'qr_range': joblib.load('models/qr_range.pkl'),
        'gbm_divergence': joblib.load('models/gbm_divergence.pkl')
    }
    print(f"Loaded {len(models)} models")
    return models

def fetch_live_data():
    """Fetch recent 1-year data + live price"""
    nifty = yf.download("^NSEI", period="1y", progress=False)
    vix = yf.download("^INDIAVIX", period="1y", progress=False)
    
    # Get live spot price
    ticker = yf.Ticker("^NSEI")
    live_price = ticker.fast_info.get('lastPrice', nifty['Close'].iloc[-1])
    
    return nifty, vix, live_price

def run_inference(models, features_df, live_price):
    """Run all model predictions"""
    latest = features_df.iloc[-1:]
    
    results = {
        'generated_at': datetime.now().isoformat(),
        'spot_price': float(live_price),
        'predictions': {}
    }
    
    # 1. Regime Prediction
    hmm_data = models['hmm_regime']
    obs = latest[['return_1d', 'volatility_20d']].values
    state = hmm_data['model'].predict(obs)[0]
    probs = hmm_data['model'].predict_proba(obs)[0]
    results['predictions']['regime'] = {
        'current': hmm_data['state_labels'][state],
        'probability': float(probs[state]),
        'all_probs': {hmm_data['state_labels'][i]: float(probs[i]) for i in range(3)}
    }
    
    # 2. Reversal Prediction
    rf_data = models['rf_reversal']
    X_rev = latest[rf_data['feature_cols']]
    rev_prob = rf_data['model'].predict_proba(X_rev)[0][1]
    results['predictions']['reversal'] = {
        'probability': float(rev_prob),
        'current_streak': int(latest['streak'].iloc[0])
    }
    
    # 3. Momentum Score
    xgb_data = models['xgb_momentum']
    X_mom = latest[xgb_data['feature_cols']]
    mom_prob = xgb_data['model'].predict_proba(X_mom)[0][1]
    results['predictions']['momentum'] = {
        'score': int(mom_prob * 100),
        'strength': 'HIGH' if mom_prob > 0.7 else 'MEDIUM' if mom_prob > 0.4 else 'LOW'
    }
    
    # 4. Range Quartiles
    qr_data = models['qr_range']
    X_range = latest[qr_data['feature_cols']]
    range_preds = {}
    for q_name, qr_model in qr_data['models'].items():
        range_preds[q_name] = float(qr_model.predict(X_range)[0] * live_price)
    results['predictions']['range'] = range_preds
    
    return results

def main():
    print("Omega Vault - Inference Run")
    print(f"Time: {datetime.now().isoformat()}")
    
    # Load models
    models = load_all_models()
    
    # Fetch data
    nifty, vix, live_price = fetch_live_data()
    print(f"Live Price: {live_price}")
    
    # Build features
    features_df = build_features(nifty, vix)
    
    # Run inference
    results = run_inference(models, features_df, live_price)
    
    # Save to JSON
    with open('client/public/data/omega_vault.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Inference complete! Results saved to omega_vault.json")

if __name__ == "__main__":
    main()
```

---

### Model Files Structure

```
models/
├── hmm_regime.pkl           # Hidden Markov Model (1.2 MB)
│   ├── model               # Trained HMM object
│   ├── state_labels        # ['TRENDING', 'MEAN_REVERTING', 'CHAOTIC']
│   └── scaler_params       # Normalization parameters
│
├── rf_reversal.pkl          # Random Forest (2.5 MB)
│   ├── model               # 200 decision trees
│   └── feature_cols        # List of feature names
│
├── xgb_momentum.pkl         # XGBoost (3.1 MB)
│   ├── model               # 200 gradient boosted trees
│   └── feature_cols        # List of feature names
│
├── qr_range.pkl             # Quantile Regression (0.8 MB)
│   ├── models              # Dict of 5 quantile models (Q10-Q90)
│   └── feature_cols        # List of feature names
│
└── gbm_divergence.pkl       # Gradient Boosting (1.8 MB)
    ├── model               # 100 boosted trees
    └── feature_cols        # List of feature names

Total: ~9.4 MB
```

---

### GitHub Actions Workflow (weekly_training.yml)

```yaml
name: Weekly Model Training

on:
  schedule:
    # Every Saturday at 00:00 UTC (5:30 AM IST)
    - cron: '0 0 * * 6'
  workflow_dispatch:  # Manual trigger

jobs:
  train:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      
      - name: Setup Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install Dependencies
        run: pip install -r engine/requirements.txt
      
      - name: Run Training Script
        run: python engine/scripts/train_all_models.py
      
      - name: Commit Trained Models
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add models/*.pkl
          git commit -m "chore: weekly model retraining [skip ci]" || exit 0
          git push
```

---

## 📐 Institutional Formulas Used

### A. Goldman Sachs Style - Probability Models

#### 1. **Black-Scholes-Merton Probability of Breach**
```python
# Probability of price touching a barrier level
from scipy.stats import norm
import numpy as np

def prob_touch_barrier(spot, barrier, sigma, T, r=0.05):
    """
    Goldman Sachs barrier option pricing methodology
    Used for calculating probability of price reaching a level
    """
    mu = r - 0.5 * sigma**2
    barrier_distance = np.log(barrier / spot)
    lambda_param = mu / sigma**2
    
    d1 = (np.log(spot / barrier) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # First passage time probability
    prob = norm.cdf(-d2) + (barrier/spot)**(2*lambda_param) * norm.cdf(-d1 + 2*lambda_param*sigma*np.sqrt(T))
    
    return np.clip(prob, 0, 1)
```

#### 2. **Jump-Diffusion Model (Merton, 1976)**
```python
# Models sudden market gaps (critical for Indian markets post-US closes)
import numpy as np

def merton_jump_diffusion_simulation(S0, r, sigma, lambda_j, mu_j, sigma_j, T, n_paths=10000):
    """
    Merton (1976) Jump-Diffusion Model
    - sigma: continuous volatility
    - lambda_j: jump intensity (avg jumps per year)
    - mu_j, sigma_j: jump size parameters
    """
    dt = T
    n_jumps = np.random.poisson(lambda_j * T, n_paths)
    jump_sizes = np.sum([np.random.normal(mu_j, sigma_j, n_paths) for _ in range(max(n_jumps))], axis=0)
    
    drift = (r - 0.5 * sigma**2 - lambda_j * (np.exp(mu_j + 0.5*sigma_j**2) - 1)) * T
    diffusion = sigma * np.sqrt(T) * np.random.normal(0, 1, n_paths)
    
    ST = S0 * np.exp(drift + diffusion + jump_sizes)
    return ST
```

### B. BlackRock Style - Risk Management

#### 3. **Conditional Value at Risk (CVaR / Expected Shortfall)**
```python
# BlackRock Aladdin-style tail risk quantification
import numpy as np

def calculate_cvar(returns, confidence=0.95):
    """
    CVaR / Expected Shortfall - Average loss beyond VaR
    BlackRock uses this for portfolio stress testing
    """
    var = np.percentile(returns, (1 - confidence) * 100)
    cvar = returns[returns <= var].mean()
    return var, cvar
```

#### 4. **Kelly Criterion Position Sizing**
```python
# Optimal bankroll allocation per trade
def kelly_criterion(win_rate, avg_win, avg_loss):
    """
    Kelly Criterion: f* = (p * b - q) / b
    where:
    - p = win probability
    - q = 1 - p
    - b = win/loss ratio
    """
    if avg_loss == 0:
        return 0.25  # Default conservative
    
    b = avg_win / abs(avg_loss)
    f_star = (win_rate * b - (1 - win_rate)) / b
    
    # Use fractional Kelly (1/4) for conservatism
    return np.clip(f_star * 0.25, 0.05, 0.25)
```

### C. DE Shaw / Renaissance Style - Statistical Edge

#### 5. **Hidden Markov Model Regime Detection**
```python
# Market regime classification using probabilistic graphical models
from hmmlearn import hmm
import numpy as np

def train_regime_hmm(returns, n_states=3):
    """
    Hidden Markov Model for regime detection
    States: 0=Trending, 1=Mean-Reverting, 2=Chaotic
    """
    model = hmm.GaussianHMM(
        n_components=n_states,
        covariance_type="full",
        n_iter=1000,
        random_state=42
    )
    
    X = returns.values.reshape(-1, 1)
    model.fit(X)
    
    hidden_states = model.predict(X)
    state_probabilities = model.predict_proba(X)
    
    return model, hidden_states, state_probabilities
```

#### 6. **Hurst Exponent for Trend Persistence**
```python
# Measures whether market is trending or mean-reverting
import numpy as np

def calculate_hurst_exponent(prices, max_lag=100):
    """
    Hurst Exponent using R/S Analysis
    H > 0.5: Trending (momentum works)
    H < 0.5: Mean-reverting (contrarian works)
    H = 0.5: Random walk
    """
    lags = range(2, max_lag)
    tau = [np.std(np.subtract(prices[lag:], prices[:-lag])) for lag in lags]
    
    # Linear fit in log-log space
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    H = poly[0]
    
    return np.clip(H, 0, 1)
```

### D. Citadel / Two Sigma Style - Options Greeks

#### 7. **Gamma Exposure (GEX) Estimation**
```python
# Dealer positioning proxy using volume patterns
def estimate_gamma_exposure(volume_series, price_series, atm_strike):
    """
    Gamma Exposure estimation using volume as proxy
    (No real OI data from yfinance, so we use volume patterns)
    """
    recent_volume = volume_series[-5:].mean()
    historical_volume = volume_series[-60:].mean()
    
    volume_ratio = recent_volume / (historical_volume + 1e-6)
    price_distance = abs(price_series.iloc[-1] - atm_strike) / atm_strike
    
    # Positive GEX = Dealers likely short gamma (dampening)
    # Negative GEX = Dealers likely long gamma (amplifying)
    gex_proxy = (volume_ratio - 1) * (1 - price_distance)
    
    return gex_proxy * 100  # Scale to -100 to +100
```

#### 8. **VIX Term Structure Analysis**
```python
# Contango/Backwardation detection for VIX futures proxy
def vix_term_structure_signal(vix_current, vix_20d_avg, vix_5d_avg):
    """
    VIX Term Structure using historical VIX as proxy
    - Contango: Near-term VIX < Longer-term (normal, sell premium)
    - Backwardation: Near-term VIX > Longer-term (stressed, buy protection)
    """
    short_term = vix_5d_avg
    long_term = vix_20d_avg
    
    term_structure = (long_term - short_term) / (long_term + 1e-6)
    
    if term_structure > 0.05:
        regime = "CONTANGO"
        signal = "SELL_PREMIUM"
    elif term_structure < -0.05:
        regime = "BACKWARDATION"
        signal = "BUY_PROTECTION"
    else:
        regime = "FLAT"
        signal = "NEUTRAL"
    
    return regime, signal, term_structure * 100
```

---

## 🎨 Dashboard Tiles (20 Total)

### Tile Grid Layout (5x4 Grid + Verdict Hero)

```
┌─────────────────────────────────────────────────────────────────────┐
│                      🌌 OMEGA VAULT HERO SECTION                    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │   VERDICT: BULLISH EDGE DETECTED                            │    │
│  │   Probability: 67.3% | Kelly Size: 18% | Risk: LOW          │    │
│  │   ████████████████░░░░░░░░ 67.3%                             │    │
│  └─────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────┤
│  📘 HOW TO USE THIS DASHBOARD (Click to Expand Guide)               │
├─────────────────────────────────────────────────────────────────────┤
│  TILE 1         │  TILE 2         │  TILE 3         │  TILE 4       │
│  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐│
│  │   Spot    │  │  │   India   │  │  │ Probability │  │  │  Regime   ││
│  │   Price   │  │  │    VIX    │  │  │   Surface   │  │  │  Beacon   ││
│  └───────────┘  │  └───────────┘  │  └───────────┘  │  └───────────┘│
├─────────────────────────────────────────────────────────────────────┤
│  TILE 5         │  TILE 6         │  TILE 7         │  TILE 8       │
│  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐│
│  │   Kelly   │  │  │    VaR    │  │  │   Hurst   │  │  │  VIX Term ││
│  │  Optimal  │  │  │   Gauge   │  │  │  Compass  │  │  │  Contour  ││
│  └───────────┘  │  └───────────┘  │  └───────────┘  │  └───────────┘│
├─────────────────────────────────────────────────────────────────────┤
│  TILE 9         │  TILE 10        │  TILE 11        │  TILE 12      │
│  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐│
│  │  Friday   │  │  │   Theta   │  │  │   Monte   │  │  │  Barrier  ││
│  │   Fear    │  │  │   Decay   │  │  │   Carlo   │  │  │  Breach   ││
│  └───────────┘  │  └───────────┘  │  └───────────┘  │  └───────────┘│
├─────────────────────────────────────────────────────────────────────┤
│  TILE 13        │  TILE 14        │  TILE 15        │  TILE 16      │
│  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐│
│  │   Streak  │  │  │   Pain    │  │  │   Range   │  │  │  Momentum ││
│  │  Reversal │  │  │   Zone    │  │  │ Quartiles │  │  │   Pulse   ││
│  └───────────┘  │  └───────────┘  │  └───────────┘  │  └───────────┘│
├─────────────────────────────────────────────────────────────────────┤
│  TILE 17        │  TILE 18        │  TILE 19        │  TILE 20      │
│  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐│
│  │    GEX    │  │  │   Event   │  │  │  Traffic  │  │  │   FOMO    ││
│  │  Cluster  │  │  │   Radar   │  │  │   Light   │  │  │   Meter   ││
│  └───────────┘  │  └───────────┘  │  └───────────┘  │  └───────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Complete Tile Specifications

### TILE 1: Spot Price Reference 🎯 {NEW}
**Category**: Market Data  
**Formula Type**: Live Feed  
**ML Required**: ❌ No (Direct API)

**What It Shows**:
- Live NIFTY/BANKNIFTY Spot Price
- Dynamic color change (Green/Red) based on LTP vs Prev Close
- Toggle button to switch between indices
- **Dynamic Verdict**: "Strong Uptrend (+0.4%)" or "Choppy / Sideways"

**User Benefit**: "Instant situational awareness - The anchor for all decisions"

---

### TILE 2: India VIX Monitor 📉 {NEW}
**Category**: Volatility  
**Formula Type**: Live Feed  
**ML Required**: ❌ No (Direct API)

**What It Shows**:
- Real-time India VIX value
- Fear Gauge: Low (<12), Normal (12-18), High (>18)
- Intraday % Change
- **Dynamic Verdict**: "Premiums Cheap (Buy)" or "Volatility Spike (Sell)"

**User Benefit**: "Know if premiums are cheap (Buy) or expensive (Sell)"

---

### TILE 3: Probability Surface 🎲
**Category**: Probability Engine  
**Formula Type**: Monte Carlo + Bayesian  
**ML Required**: ❌ No (Pure Statistical)

**What It Shows**:
- 3D probability surface for next 5 days
- Color gradient: Green (bullish zones) → Red (bearish zones)
- Contour lines at 25%, 50%, 75% probability levels
- **Dynamic Verdict**: "Skew: Call Side (+2%)" or "Skew: Balanced"

**Formula**:
```python
# 10,000 Monte Carlo paths
paths = merton_jump_diffusion_simulation(spot, r, sigma, lambda_j, mu_j, sigma_j, T)
prob_above_strike = np.mean(paths > strike)
```

**User Benefit**: "See WHERE the price is most likely to go, not just UP or DOWN"

---

### TILE 4: Regime Beacon 🚦
**Category**: Market State  
**Formula Type**: Hidden Markov Model + GARCH  
**ML Required**: ✅ Yes (HMM Training)

**What It Shows**:
- Current market regime with probability
- Transition probabilities to other regimes
- Historical regime timeline (last 20 days)
- **Dynamic Verdict**: "Trending (Good for Buyers)" or "Chaotic (Stay Away)"

**Regimes**:
| Regime | Color | Description | Best Strategy |
|--------|-------|-------------|---------------|
| TRENDING | 🟢 Green | Strong directional moves | Directional options |
| MEAN-REVERTING | 🟡 Yellow | Price oscillating around mean | Iron condors |
| CHAOTIC | 🔴 Red | High uncertainty, jumps | Stay cash / hedge |

**Formula**: HMM with Gaussian emissions trained on daily returns

---

### TILE 5: Kelly Optimal 💰
**Category**: Position Sizing  
**Formula Type**: Kelly Criterion  
**ML Required**: ❌ No

**What It Shows**:
- Optimal position size as % of capital
- Full Kelly vs 1/4 Kelly comparison
- Risk-adjusted return expectation

**Display**:
```
Full Kelly: 32%
Quarter Kelly (Recommended): 8%

If Capital = ₹10,00,000
Invest: ₹80,000 in this trade
```

**User Benefit**: "Know EXACTLY how much to risk, mathematically optimized"

---

### TILE 6: VaR Gauge ⚠️
**Category**: Risk Management  
**Formula Type**: Historical VaR + CVaR  
**ML Required**: ❌ No

**What It Shows**:
- 95% VaR: "You won't lose more than X with 95% confidence"
- 99% VaR: "Worst-case 1-in-100 days scenario"
- CVaR (Expected Shortfall): "Average loss in tail events"

**Gauge Colors**:
| VaR Level | Color | Interpretation |
|-----------|-------|----------------|
| < 1.5% | 🟢 Low Risk | Normal volatility |
| 1.5% - 3% | 🟡 Moderate | Elevated caution |
| > 3% | 🔴 High Risk | Reduce position size |

---

### TILE 7: Hurst Compass 🧭
**Category**: Trend Persistence  
**Formula Type**: R/S Analysis  
**ML Required**: ❌ No

**What It Shows**:
- Hurst Exponent value (0 to 1)
- Trend persistence interpretation
- Strategy recommendation

**Quadrants**:
```
           TRENDING
              ↑
    H > 0.6 = Momentum
              │
REVERTING ←───┼───→ RANDOM
              │
    H < 0.4 = Contrarian
              ↓
```

**User Benefit**: "Know if momentum or mean-reversion strategies will work"

---

### TILE 8: VIX Term Contour 📈
**Category**: Volatility Analysis  
**Formula Type**: Term Structure  
**ML Required**: ❌ No

**What It Shows**:
- VIX term structure visualization
- Contango/Backwardation signal
- Premium selling opportunity window

**Signals**:
| Structure | Signal | Action |
|-----------|--------|--------|
| CONTANGO | 🟢 Sell Premium | Write options (theta decay favor) |
| BACKWARDATION | 🔴 Buy Protection | Buy puts (tail risk elevated) |
| FLAT | 🟡 Neutral | Normal positioning |

---

### TILE 9: Friday Fear Index 🌙
**Category**: Gap Risk  
**Formula Type**: Empirical + Statistical  
**ML Required**: ❌ No

**What It Shows**:
- Weekend gap probability
- Historical Friday-to-Monday gap distribution
- Gap size expectation (points)

**Formula**:
```python
# Historical Friday-to-Monday gaps
gaps = monday_open - friday_close
gap_probability = np.percentile(np.abs(gaps), [50, 75, 90, 95])
```

**User Benefit**: "Know if holding over the weekend is worth the risk"

---

### TILE 10: Theta Decay Curves ⏰
**Category**: Options Greeks  
**Formula Type**: Black-Scholes Theta  
**ML Required**: ❌ No

**What It Shows**:
- Theta decay acceleration by DTE
- Optimal entry/exit DTEs
- "Theta Cliff" warning zones

**Visualization**:
```
Theta Decay (% per day)
│
│     ◄── Acceleration Zone
│        ╱
│       ╱
│      ╱
│─────╱───────────────── 
│               ↑
└─────────────────────→ DTE
      7   5   3   1
```

---

### TILE 11: Monte Carlo Cones 🔮
**Category**: Price Projection  
**Formula Type**: Monte Carlo Simulation  
**ML Required**: ❌ No

**What It Shows**:
- Price cones at 1σ, 2σ, 3σ levels
- 5-day forward projection
- Probability at each price level

**Display**:
```
                    ╱ 3σ (99.7%)
                   ╱  2σ (95%)
                  ╱   1σ (68%)
    SPOT ────────●────╲
                  ╲   1σ
                   ╲  2σ
                    ╲ 3σ
    └────┴────┴────┴────┴────→
    D+0  D+1  D+2  D+3  D+4
```

---

### TILE 12: Barrier Breach Probability 🚧
**Category**: Options Pricing  
**Formula Type**: Black-Scholes Barrier  
**ML Required**: ❌ No

**What It Shows**:
- Probability of touching key strike levels
- Dynamic barrier visualization
- Risk-reward for barrier options

**Barriers Calculated**:
- ATM ± 1%
- ATM ± 2%
- ATM ± 3%

---

### TILE 13: Streak Reversal 🔄
**Category**: Statistical Pattern  
**Formula Type**: Empirical + Bayesian  
**ML Required**: ✅ Yes (Random Forest)

**What It Shows**:
- Current streak (consecutive up/down days)
- Historical reversal probability after similar streaks
- ML-enhanced reversal confidence

**Formula**:
```python
# After 3 consecutive up days, probability of down day
streak_reversal_prob = model.predict_proba(streak_features)
```

---

### TILE 14: Pain Zone 🎯
**Category**: Market Structure  
**Formula Type**: Max Pain + Volume Profile  
**ML Required**: ❌ No

**What It Shows**:
- Estimated max pain zone (volume-weighted center)
- Price attraction levels
- Magnetic price targets

**Calculation**:
```python
# Volume-weighted average price zones
pain_zone = np.average(price_levels, weights=volume_at_levels)
attraction_strength = volume_concentration_ratio
```

---

### TILE 15: Range Quartiles 📊
**Category**: Statistical Range  
**Formula Type**: Quantile Regression  
**ML Required**: ✅ Yes (Quantile Regression)

**What It Shows**:
- Expected range (Q25 to Q75)
- Extreme range (Q10 to Q90)
- Current price position within range

**Visualization**:
```
Q10 ─────┬─────────────────┬───── Q90
         │     ┌───────┐   │
         │ Q25 │ SPOT  │Q75│
         │     └───────┘   │
         └─────────────────┘
```

---

### TILE 16: Momentum Pulse 💓
**Category**: Technical  
**Formula Type**: RSI + MACD + Momentum Composite  
**ML Required**: ✅ Yes (Gradient Boosting)

**What It Shows**:
- Composite momentum score (0-100)
- Overbought/Oversold zones
- Momentum divergence detection

**Components**:
- RSI (14-day)
- MACD Signal Line Cross
- Rate of Change (20-day)
- Stochastic K/D

---

### TILE 17: GEX Cluster 🔥
**Category**: Dealer Positioning  
**Formula Type**: Volume-Proxy GEX  
**ML Required**: ❌ No (Volume Proxy)

**What It Shows**:
- Estimated dealer gamma exposure
- Expected volatility dampening/amplification
- Key gamma flip levels

**Interpretation**:
| GEX | Effect | Price Behavior |
|-----|--------|----------------|
| +High | Dampening | Mean-reverting |
| -High | Amplifying | Trend extension |
| Near Zero | Neutral | Normal volatility |

---

### TILE 18: Event Radar 📡
**Category**: Calendar  
**Formula Type**: Empirical Event Impact  
**ML Required**: ❌ No

**What It Shows**:
- Upcoming market events (RBI, Expiry, etc.)
- Historical impact of similar events
- Volatility expansion expectation

**Events Tracked**:
- Monthly expiry
- Weekly expiry
- RBI policy days
- US Fed announcements
- Budget day (annual)

---

### TILE 19: Trade Traffic Light 🚦 {NEW}
**Category**: Beginner Logic  
**Formula Type**: Multi-Factor Confluence  
**ML Required**: ✅ Yes (Uses Regime + Momentum Outputs)

**What It Shows**:
- **GO (Green)**: Market is safe for new entries
- **WAIT (Yellow)**: Mixed signals, reduce size
- **STOP (Red)**: Dangerous conditions (Choppy/High Vol)

**Logic**:
- **Green**: Regime=Trending AND VIX<20 AND Momentum>60
- **Red**: Regime=Chaotic OR VIX>24
- **Yellow**: Everything else

**User Benefit**: "Simple Yes/No answer for 'Should I trade today?'"

---

### TILE 20: FOMO Meter 😱 {NEW}
**Category**: Psychology / Risk  
**Formula Type**: Mean Reversion Logic  
**ML Required**: ❌ No

**What It Shows**:
- Gauge measuring how "over-extended" the price is
- Prevents buying at the top or selling at the bottom

**Logic**:
- **EXTREME FOMO (Don't Buy)**: RSI > 75 OR Price > Upper BB (2σ)
- **HIGH RISK**: RSI 65-75
- **NEUTRAL**: RSI 35-65
- **EXTREME PANIC (Don't Sell)**: RSI < 25 OR Price < Lower BB (2σ)

**User Benefit**: "Saves you from bad entries driven by emotion"

## 🎨 Design Theme: TRON LEGACY × JARVIS

### Color Palette

```css
:root {
  /* Primary Colors - TRON Legacy Cyan */
  --tron-cyan: #00FFFF;
  --tron-cyan-glow: rgba(0, 255, 255, 0.3);
  --tron-orange: #FF6600;
  --tron-orange-glow: rgba(255, 102, 0, 0.3);
  
  /* Background - Deep Space */
  --bg-primary: #0A0A0F;
  --bg-secondary: #12121A;
  --bg-card: #1A1A25;
  --bg-card-hover: #222230;
  
  /* JARVIS-style Accent */
  --jarvis-blue: #4A90D9;
  --jarvis-gold: #FFD700;
  
  /* Grid Lines */
  --grid-line: rgba(0, 255, 255, 0.1);
  --grid-highlight: rgba(0, 255, 255, 0.3);
  
  /* Text */
  --text-primary: #FFFFFF;
  --text-secondary: #8892B0;
  --text-muted: #4A5568;
  
  /* Signals */
  --signal-bullish: #00FF88;
  --signal-bearish: #FF4444;
  --signal-neutral: #888888;
}
```

### Background Animations

```css
/* Animated Grid Background - TRON Style */
.tron-grid-background {
  background-image: 
    linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: grid-pulse 4s ease-in-out infinite;
}

@keyframes grid-pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

/* Floating Particles - JARVIS Hologram */
.particle-field::before {
  content: '';
  position: absolute;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle at 50% 50%,
    rgba(0, 255, 255, 0.1) 0%,
    transparent 50%
  );
  animation: particle-drift 20s linear infinite;
}

@keyframes particle-drift {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Scan Line Effect */
.scan-line::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--tron-cyan),
    transparent
  );
  animation: scan 3s linear infinite;
}

@keyframes scan {
  0% { top: -2px; opacity: 0; }
  50% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}
```

### Tile Styling

```css
/* Glass Morphism Tiles */
.omega-tile {
  background: rgba(26, 26, 37, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 12px;
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.omega-tile:hover {
  border-color: var(--tron-cyan);
  box-shadow: 
    0 8px 40px rgba(0, 255, 255, 0.2),
    0 0 20px rgba(0, 255, 255, 0.1);
  transform: translateY(-2px);
}

/* Neon Glow Effect on Hover */
.omega-tile::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 14px;
  background: linear-gradient(
    45deg,
    var(--tron-cyan),
    var(--tron-orange),
    var(--tron-cyan)
  );
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.omega-tile:hover::before {
  opacity: 0.5;
  animation: border-glow 2s linear infinite;
}

@keyframes border-glow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

### Dark/Light Mode

```css
/* Dark Mode (Default) */
[data-theme="dark"] {
  --bg-primary: #0A0A0F;
  --text-primary: #FFFFFF;
  --tron-cyan: #00FFFF;
}

/* Light Mode - Frosted Glass */
[data-theme="light"] {
  --bg-primary: #F0F4F8;
  --bg-secondary: #FFFFFF;
  --bg-card: rgba(255, 255, 255, 0.9);
  --text-primary: #1A202C;
  --text-secondary: #4A5568;
  --tron-cyan: #0077B6;
  --grid-line: rgba(0, 119, 182, 0.1);
}

/* Light mode keeps the futuristic feel with blue accents */
[data-theme="light"] .omega-tile {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(0, 119, 182, 0.2);
}
```

---

## 🛠️ Technology Stack

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Vite** | 5.4.x | Build tool & dev server |
| **React** | 18.3.x | UI framework |
| **TypeScript** | 5.3.x | Type safety |
| **Tailwind CSS** | 3.4.x | Utility styling |
| **Framer Motion** | 11.x | Animations |
| **Recharts** | 2.15.x | Charting library |
| **React Query** | 5.x | Data fetching |
| **Three.js** | 0.165.x | 3D probability surface (optional) |

### Backend (Python)

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12+ | Runtime |
| **yfinance** | 0.2.x | Data source (SOLE source of truth) |
| **pandas** | 2.2.x | Data manipulation |
| **numpy** | 1.26.x | Numerical computing |
| **scipy** | 1.13.x | Statistical functions |
| **scikit-learn** | 1.4.x | ML models |
| **hmmlearn** | 0.3.x | Hidden Markov Models |
| **joblib** | 1.4.x | Model persistence |

### Infrastructure (Zero Cost)

| Component | Tier | Usage |
|-----------|------|-------|
| **GitHub Actions** | Free | CI/CD, scheduled inference |
| **Cloudflare Pages** | Free | Frontend hosting |
| **GitHub Repo** | Free | Model storage |

---

## 📁 Project Structure

```
omega-vault/
├── client/                          # React Frontend (Vite)
│   ├── public/
│   │   ├── data/
│   │   │   └── omega_vault.json    # Generated predictions
│   │   ├── favicon.svg             # Cyan Ω icon
│   │   └── og-image.png            # Social preview
│   ├── src/
│   │   ├── components/
│   │   │   ├── tiles/              # 16 tile components
│   │   │   │   ├── ProbabilitySurface.tsx
│   │   │   │   ├── RegimeBeacon.tsx
│   │   │   │   ├── KellyOptimal.tsx
│   │   │   │   ├── VaRGauge.tsx
│   │   │   │   ├── HurstCompass.tsx
│   │   │   │   ├── VIXTermContour.tsx
│   │   │   │   ├── FridayFear.tsx
│   │   │   │   ├── ThetaDecay.tsx
│   │   │   │   ├── MonteCarloCones.tsx
│   │   │   │   ├── BarrierBreach.tsx
│   │   │   │   ├── StreakReversal.tsx
│   │   │   │   ├── PainZone.tsx
│   │   │   │   ├── RangeQuartiles.tsx
│   │   │   │   ├── MomentumPulse.tsx
│   │   │   │   ├── GEXCluster.tsx
│   │   │   │   └── EventRadar.tsx
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── TileGrid.tsx
│   │   │   ├── effects/
│   │   │   │   ├── TronGrid.tsx
│   │   │   │   ├── ScanLine.tsx
│   │   │   │   └── ParticleField.tsx
│   │   │   └── VerdictHero.tsx
│   │   ├── hooks/
│   │   │   └── useOmegaData.ts
│   │   ├── lib/
│   │   │   ├── types.ts
│   │   │   └── formatters.ts
│   │   ├── styles/
│   │   │   └── globals.css
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── package.json
│
├── engine/                          # Python Backend
│   ├── scripts/
│   │   ├── data_fetcher.py         # yfinance data ingestion
│   │   ├── feature_engineer.py     # Technical indicators
│   │   ├── probability_models.py   # Monte Carlo, BSM
│   │   ├── regime_detector.py      # HMM training
│   │   ├── risk_calculator.py      # VaR, CVaR, Kelly
│   │   ├── ml_models.py            # RF, XGBoost training
│   │   ├── infer.py                # Daily inference
│   │   └── run_all.py              # Master script
│   ├── models/                      # Trained model files
│   │   ├── hmm_regime.pkl
│   │   ├── rf_momentum.pkl
│   │   ├── qr_range.pkl
│   │   └── xgb_reversal.pkl
│   ├── data/
│   │   ├── NSEI_daily.csv
│   │   ├── NSEBANK_daily.csv
│   │   └── INDIAVIX_daily.csv
│   └── requirements.txt
│
├── .github/
│   └── workflows/
│       ├── weekly_training.yml     # Saturday model retraining
│       └── daily_inference.yml     # M-F 30-min inference
│
├── docs/
│   └── SEBI_COMPLIANCE.md
│
└── README.md
```

---

## 🚀 Training & Inference Pipeline

### Weekly Training (Saturdays)

```mermaid
graph LR
    A[yfinance.download] --> B[NIFTY + BANKNIFTY + VIX<br/>2005-Present]
    B --> C[Feature Engineering<br/>50+ features]
    C --> D{Train Models}
    D --> E[HMM Regime]
    D --> F[RF Momentum]
    D --> G[XGBoost Reversal]
    D --> H[Quantile Range]
    E --> I[Save to models/]
    F --> I
    G --> I
    H --> I
    I --> J[Commit to GitHub]
```

**Training Time**: ~10-15 minutes  
**Model Size**: ~15 MB total  
**Data Period**: 2005 to present (~20 years)

### Daily Inference (Every 30 min, Market Hours)

```mermaid
graph LR
    A[Load Trained Models] --> B[Fetch Recent Data<br/>yfinance 1y + live]
    B --> C[Build Features]
    C --> D[Run Inference]
    D --> E[Monte Carlo<br/>10,000 paths]
    D --> F[HMM Predict<br/>Current regime]
    D --> G[Kelly Calculate<br/>Position size]
    D --> H[VaR Estimate<br/>Risk gauge]
    E --> I[omega_vault.json]
    F --> I
    G --> I
    H --> I
    I --> J[Commit & Deploy]
```

**Inference Time**: ~30 seconds  
**Update Frequency**: Every 30 min (9:15 AM - 3:30 PM IST)

---

## 📈 User Benefit Summary

| Tile | User Benefit | Confidence Boost |
|------|--------------|------------------|
| **Probability Surface** | Know WHERE price will likely go | "I see the odds, not guesses" |
| **Regime Beacon** | Know WHEN your strategy works | "I trade WITH the market flow" |
| **Kelly Optimal** | Know HOW MUCH to risk | "My sizing is mathematically optimal" |
| **VaR Gauge** | Know your WORST CASE | "I sleep better knowing my max loss" |
| **Hurst Compass** | Know IF trend will continue | "I know when to ride or fade" |
| **VIX Term Contour** | Know WHEN to sell premium | "I collect premium at the right time" |
| **Friday Fear** | Know WEEKEND gap risk | "I don't hold blindly over weekends" |
| **Theta Decay** | Know WHEN options bleed | "I time my entries perfectly" |
| **Monte Carlo Cones** | See PROBABILITY RANGES | "I see all possible outcomes" |
| **Barrier Breach** | Know STRIKE touch odds | "I price my stop losses correctly" |
| **Streak Reversal** | Know WHEN to bet against streak | "I catch reversals early" |
| **Pain Zone** | Know WHERE price gets attracted | "I trade to where price wants to go" |
| **Range Quartiles** | Know EXPECTED movement | "I set realistic targets" |
| **Momentum Pulse** | Know CONVICTION strength | "I trade only strong setups" |
| **GEX Cluster** | Know DEALER positioning | "I trade with smart money" |
| **Event Radar** | Know WHAT's coming | "I'm never surprised by events" |

---

## 🛡️ SEBI Compliance

> **DISCLAIMER**: This dashboard provides **statistical analysis and probability calculations** for **educational purposes only**. It does **NOT** provide:
> - Investment advice
> - Buy/Sell recommendations
> - Guaranteed returns
> - Stock tips

### Compliance Measures

1. **No Recommendations**: All outputs are probabilities, not "BUY" or "SELL" signals
2. **Risk Warnings**: Every tile shows associated risks
3. **Past Performance Disclaimer**: Historical accuracy is displayed but not guaranteed
4. **Educational Labeling**: Clear "For Educational Use Only" badges
5. **No SEBI Registration Required**: As per SEBI Investment Adviser Regulations 2013, statistical tools don't require registration

---

## 💰 Revenue Model

### Ad-Supported (Zero User Cost)

| Ad Placement | Size | Network |
|--------------|------|---------|
| Header banner | 728×90 | Adsterra |
| Sidebar | 300×250 | Adsterra |
| Between tiles | Native | Adsterra |
| Mobile bottom | 320×50 | Adsterra |

### Traffic Potential

| Metric | Estimate |
|--------|----------|
| **Target Market** | 50M+ Indian F&O traders |
| **TAM Capture** | 0.1% = 50,000 daily users |
| **Page Views/User** | 5 (multiple tiles) |
| **Daily Page Views** | 250,000 |
| **RPM (India)** | $1-3 |
| **Monthly Revenue** | $7,500 - $22,500 |

---

## 🌊 High Traffic Potential

### Why Users Will Flock

1. **Unique Value Prop**: No other free tool offers probability-first options analytics
2. **Premium Feel**: Institutional-grade formulas, futuristic UI
3. **Trust Building**: Transparent formulas, no hidden "secret sauce"
4. **Community Growth**: Share-worthy screenshots, social buzz potential
5. **SEO Advantage**: "NIFTY probability calculator", "BANKNIFTY VaR" keywords
6. **Mobile PWA**: Installable on phones for quick checks

### Competition Gap

| Existing Tools | Our Advantage |
|----------------|---------------|
| TradingView | No probability models, charting-only |
| Sensibull | Options-focused but premium paywall |
| Opstra | Complex, not beginner-friendly |
| Generic screeners | Stock-focused, not F&O |

**Omega Vault fills the gap**: **Free + Probability-focused + Options-specific + Premium UI**

---

## ⚡ Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/yourusername/omega-vault.git
cd omega-vault

# 2. Install frontend dependencies
cd client
npm install

# 3. Install Python dependencies
cd ../engine
pip install -r requirements.txt

# 4. Run data pipeline
python scripts/run_all.py

# 5. Start frontend
cd ../client
npm run dev

# Open http://localhost:5173
```

### Production Deployment

```bash
# Auto-deploys via GitHub Actions
git push origin main
# → weekly_training.yml runs on Saturdays
# → daily_inference.yml runs every 30 min M-F
# → Cloudflare Pages auto-deploys on commit
```

---

## 📞 Summary

**Tradyxa Omega Vault** is a **flagship, enterprise-level** probabilistic intelligence dashboard for **NIFTY and BANKNIFTY options traders**. It combines:

- **Goldman Sachs-style probability models**
- **BlackRock-style risk management (VaR, Kelly)**
- **DE Shaw-style regime detection (HMM)**
- **Citadel-style Greeks estimation**

All powered by **yfinance as the sole data source**, with **zero infrastructure cost**, and delivered through a **stunning TRON Legacy × JARVIS themed UI**.

**Sleep better. Trade smarter. Trust the probabilities.**

---

*Version 1.0.0 | Last Updated: December 2025 | For Educational Use Only*
