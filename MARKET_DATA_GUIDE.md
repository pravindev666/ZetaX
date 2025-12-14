# Indian Market Data Libraries Guide

This guide details how to implement and use **nsepython**, **jugaad_data**, and **OpenBB** for the Tradyxa RubiX project.

## 🚀 Quick Comparison

| Library | Best For | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **nsepython** | **Live Option Chain**, OI Data | Connects directly to NSE API, minimal lag. | Can be blocked if scraped too aggressively. |
| **jugaad_data** | **Historical Data**, Caching | Native caching, clean API, supports new NSE site. | Live data might have slight delays vs direct API. |
| **OpenBB** | **Deep Research**, Global Data | Massive ecosystem, AI integration, 30+ sources. | Heavy installation, overkill for simple price fetching. |
| **nsetools** | *Deprecated* | Simple legacy API. | **Broken** on new NSE website. Avoid. |

---

## 1. nsepython (Best for Live Options & OI)

Use this to fetch the **Option Chain** for your "Pain Zone" and "Probability Surface" tiles.

### Installation
```bash
pip install nsepython
```

### Usage: Fetching Option Chain

```python
from nsepython import *

# 1. Get raw Option Chain JSON
nifty_oc = nse_optionchain_scrapper('NIFTY')

# 2. Get specific strike data (e.g., Live Price, OI)
# Note: 'expiry_date' format must match NSE (e.g., "28-Mar-2024")
def get_oi_data(symbol, expiry):
    payload = nse_optionchain_scrapper(symbol)
    col_names = ['Strike Price','CE Open Interest','PE Open Interest','CE LTP','PE LTP']
    try:
        oi_data = nse_optionchain_pandas(payload, expiry, col_names)
        return oi_data
    except Exception as e:
        print(f"Error fetching OI: {e}")
        return None

# Example Run
# print(get_oi_data("NIFTY", "28-Mar-2024"))
```

### Usage: Live F&O Quote
```python
# Get full quote for a symbol
quote = nse_quote_ltp("BANKNIFTY", "latest", "MCX") # or other types
print(quote)
```

---

## 2. jugaad_data (Best for Historical Caching)

Use this to backfill specific missing historical data without hitting Yahoo Finance rate limits.

### Installation
```bash
pip install jugaad-data
```

### Usage: Fetching Historical Index Data

```python
from datetime import date
from jugaad_data.nse import index_csv, stock_csv

# Download NIFTY history to a file (Automatic caching)
# This saves 'NIFTY 50.csv' in your current directory
index_csv(symbol="NIFTY 50", from_date=date(2023, 1, 1), to_date=date(2024, 1, 1), output_dir="./data")

# Read it with pandas
import pandas as pd
df = pd.read_csv("./data/NIFTY 50.csv")
print(df.head())
```

---

## 3. OpenBB (Best for Deep Research)

Use the SDK for complex correlations (e.g., "Is NIFTY correlated with DXY?"). Note: This is a heavy library.

### Installation
```bash
pip install openbb
```

### Usage: Python SDK (v4+)

```python
from openbb import obb

# Fetch Historical Price
# provider='yfinance' is reliable for Indian stocks (suffix .NS)
df = obb.equity.price.historical("RELIANCE.NS", provider="yfinance")
print(df.to_dataframe())

# Advanced: Fundamental Analysis (P/E, Ratios)
# Note: Requires API keys for some providers (FMP, AlphaVantage)
# fundamentals = obb.equity.fundamental.metrics("INFY.NS", provider="yfinance")
```

---

## 📅 Recommended Implementation Plan

For **Tradyxa RubiX**, we recommend this hybrid approach:

1.  **Keep `yfinance`** for reliable OHLCV history (Market Regime, Momentum).
2.  **Add `nsepython`** specifically for the **Option Chain** fetching.
    *   *Why?* Calculating Max Pain and Gamma Exposure requires accurate Open Interest data, which `yfinance` does not provide well.
3.  **Ignore `nsetools`**, it is outdated.
