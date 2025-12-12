import { MarketDataState, DataPoint, TrendDirection } from '../types';

// Base path for generated JSON files from Python inference
const JSON_DATA_BASE = '/data';

// Fallback mock data generator (for dev/offline mode)
const generateHistory = (points: number, start: number, volatility: number, trend: TrendDirection = 'neutral') => {
  let current = start;
  const bias = trend === 'up' ? 1 : trend === 'down' ? -1 : 0;

  return Array.from({ length: points }, (_, i) => {
    const noise = (Math.random() - 0.5) * volatility;
    const drift = bias * (volatility * 0.8);
    current += noise + drift;
    return { time: `${i}m`, value: current };
  });
};

/**
 * Fetch live market data from the Python inference JSON.
 * Falls back to mock data if fetch fails.
 */
export async function fetchMarketDataFromJSON(index: 'NIFTY' | 'BANKNIFTY'): Promise<MarketDataState | null> {
  try {
    // Fetch index-specific JSON file
    const jsonPath = `${JSON_DATA_BASE}/rubix_${index.toLowerCase()}.json`;
    const response = await fetch(`${jsonPath}?t=${Date.now()}`);
    if (!response.ok) {
      console.warn(`Failed to fetch ${jsonPath}, using mock data`);
      return null;
    }

    const data = await response.json();

    // Validate structure
    if (!data.tiles || !data.hero) {
      console.warn('Invalid JSON structure, using mock data');
      return null;
    }

    // Convert JSON to MarketDataState format
    // The JSON from infer.py already matches our types.ts structure!
    return {
      indexName: data.indexName || index,
      timestamp: data.timestamp || new Date().toLocaleTimeString(),
      hero: {
        verdictTitle: data.hero.verdictTitle,
        verdictSubtitle: data.hero.verdictSubtitle,
        bullishProbability: data.hero.bullishProbability,
        riskLevel: data.hero.riskLevel,
        riskVerdict: data.hero.riskVerdict,
        kellySize: data.hero.kellySize,
        kellyVerdict: data.hero.kellyVerdict,
      },
      tiles: {
        spotPrice: enhanceDataPoint(data.tiles.spotPrice),
        indiaVix: enhanceDataPoint(data.tiles.indiaVix),
        probabilitySurface: enhanceDataPoint(data.tiles.probabilitySurface),
        regimeBeacon: enhanceDataPoint(data.tiles.regimeBeacon),
        kellyOptimal: enhanceDataPoint(data.tiles.kellyOptimal),
        varGauge: enhanceDataPoint(data.tiles.varGauge),
        hurstCompass: enhanceDataPoint(data.tiles.hurstCompass),
        vixTerm: enhanceDataPoint(data.tiles.vixTerm),
        fridayFear: enhanceDataPoint(data.tiles.fridayFear),
        thetaDecay: enhanceDataPoint(data.tiles.thetaDecay),
        monteCarlo: enhanceDataPoint(data.tiles.monteCarlo),
        barrierBreach: enhanceDataPoint(data.tiles.barrierBreach),
        streakReversal: enhanceDataPoint(data.tiles.streakReversal),
        painZone: enhanceDataPoint(data.tiles.painZone),
        rangeQuartiles: enhanceDataPoint(data.tiles.rangeQuartiles),
        momentumPulse: enhanceDataPoint(data.tiles.momentumPulse),
        gexCluster: enhanceDataPoint(data.tiles.gexCluster),
        eventRadar: enhanceDataPoint(data.tiles.eventRadar),
        trafficLight: enhanceDataPoint(data.tiles.trafficLight),
        fomoMeter: enhanceDataPoint(data.tiles.fomoMeter),
      },
      // Pass through overallVerdict from Python
      overallVerdict: data.overallVerdict || null
    };
  } catch (error) {
    console.error('Error fetching market data:', error);
    return null;
  }
}

/**
 * Generate mock history for sparklines if not provided
 */
function generateFallbackHistory(value: number, trend: string = 'neutral', points: number = 20): { time: string, value: number }[] {
  let current = value;
  const volatility = Math.abs(value * 0.002); // 0.2% volatility
  const bias = trend === 'up' ? 1 : trend === 'down' ? -1 : 0;

  return Array.from({ length: points }, (_, i) => {
    const noise = (Math.random() - 0.5) * volatility;
    const drift = bias * (volatility * 0.5);
    current += noise + drift;
    return { time: `${i}m`, value: current };
  });
}

/**
 * Enhance data point with default values for any missing fields
 */
function enhanceDataPoint(point: any): DataPoint {
  const numValue = typeof point?.value === 'number' ? point.value :
    typeof point?.value === 'string' ? parseFloat(point.value.replace(/[^\d.-]/g, '')) || 0 : 0;

  return {
    id: point?.id || 'unknown',
    label: point?.label || 'Unknown',
    value: point?.value ?? '—',
    unit: point?.unit,
    change: point?.change,
    trend: point?.trend,
    verdict: point?.verdict || '',
    // Generate fallback history if not provided and value is numeric
    history: point?.history || (numValue > 0 ? generateFallbackHistory(numValue, point?.trend) : undefined),
    meta: point?.meta,
  };
}

/**
 * Get market data - tries JSON first, falls back to mock.
 * This is the main export used by the dashboard.
 */
export const getMarketData = (index: 'NIFTY' | 'BANKNIFTY'): MarketDataState => {
  // Return mock data synchronously (for immediate render)
  // The async version will update the state after
  return getMockMarketData(index);
};

/**
 * Async version that tries to load real data
 */
export const getMarketDataAsync = async (index: 'NIFTY' | 'BANKNIFTY'): Promise<MarketDataState> => {
  const liveData = await fetchMarketDataFromJSON(index);
  if (liveData) {
    return liveData;
  }
  return getMockMarketData(index);
};

/**
 * Mock data generator for development/fallback
 */
export const getMockMarketData = (index: 'NIFTY' | 'BANKNIFTY'): MarketDataState => {
  const isNifty = index === 'NIFTY';
  const basePrice = isNifty ? 22150 : 47500;

  // Simulation of current state
  const isBullish = Math.random() > 0.4;

  return {
    indexName: index,
    timestamp: new Date().toLocaleTimeString(),
    hero: {
      verdictTitle: isBullish ? "BULLISH EDGE DETECTED" : "BEARISH DIVERGENCE",
      verdictSubtitle: isBullish ? "Momentum favors longs. Volatility is contracting." : "Distribution active. Beware of bull traps.",
      bullishProbability: isBullish ? 68 : 32,
      riskLevel: isBullish ? 34 : 76,
      riskVerdict: isBullish ? "Conditions Optimal" : "High Volatility Warning",
      kellySize: isBullish ? 18 : 5,
      kellyVerdict: isBullish ? "Aggressive Allocation" : "Preserve Capital",
    },
    tiles: {
      // --- Row 1 ---
      spotPrice: {
        id: 'spot',
        label: 'Current Level',
        value: Math.floor(basePrice + (Math.random() * 50)),
        change: isBullish ? 0.42 : -0.35,
        trend: isBullish ? 'up' : 'down',
        verdict: isBullish ? "Above VWAP" : "Below VWAP",
        history: generateHistory(20, basePrice, 15, isBullish ? 'up' : 'down')
      },
      indiaVix: {
        id: 'vix',
        label: 'Fear Gauge (VIX)',
        value: 12.4,
        change: -1.2,
        trend: 'down',
        verdict: "Safe Zone < 15",
        history: generateHistory(20, 12.5, 0.2, 'down')
      },
      probabilitySurface: {
        id: 'probs',
        label: 'Option Skew',
        value: isBullish ? 'Call Bias' : 'Put Bias',
        verdict: isBullish ? "Bulls are paying up" : "Puts expensive",
        meta: { call: 60, put: 40 }
      },
      regimeBeacon: {
        id: 'regime',
        label: 'Market Regime',
        value: 'TRENDING',
        verdict: "High Confidence",
        meta: { type: 'trending' }
      },
      kellyOptimal: {
        id: 'kelly',
        label: 'Bet Size',
        value: isBullish ? '18%' : '5%',
        verdict: isBullish ? "Aggressive Allocation" : "Defensive Mode"
      },

      // --- Row 2 ---
      varGauge: {
        id: 'var',
        label: 'Max Daily Loss',
        value: '-1.8%',
        verdict: "Low Risk (<2%)"
      },
      hurstCompass: {
        id: 'hurst',
        label: 'Trend Strength',
        value: 0.62,
        verdict: "Trend Persisting"
      },
      vixTerm: {
        id: 'vixterm',
        label: 'Volatility Term',
        value: 'Normal',
        verdict: "No Panic Detected",
        history: [{ time: 'Spot', value: 12.4 }, { time: 'M1', value: 13.1 }, { time: 'M2', value: 14.2 }]
      },
      fridayFear: {
        id: 'fear',
        label: 'Weekend Risk',
        value: 'Low',
        verdict: "Gap Risk Minimal"
      },
      thetaDecay: {
        id: 'theta',
        label: 'Time Decay',
        value: -45.2,
        unit: 'pts/day',
        verdict: "Seller's Advantage"
      },

      // --- Row 3 ---
      monteCarlo: {
        id: 'mc',
        label: 'Prediction (1hr)',
        value: 'Stable',
        verdict: "Within 1σ Range",
        history: generateHistory(30, basePrice, 40, 'neutral')
      },
      barrierBreach: {
        id: 'barrier',
        label: 'Touch Probability',
        value: '64%',
        verdict: "Target Likely"
      },
      streakReversal: {
        id: 'streak',
        label: 'Reversal Chance',
        value: 'Low',
        verdict: "Don't Fade Moves"
      },
      painZone: {
        id: 'pain',
        label: 'Expiry Pin',
        value: isNifty ? 22200 : 47600,
        verdict: `Magnet: ${isNifty ? 22200 : 47600}`
      },
      rangeQuartiles: {
        id: 'range',
        label: 'Expected Range',
        value: '+/- 120',
        verdict: "Wide Expansion"
      },

      // --- Row 4 ---
      momentumPulse: {
        id: 'momentum',
        label: 'Momentum',
        value: isBullish ? '+4.2' : '-3.1',
        verdict: isBullish ? "Accelerating Up" : "Momentum Fading",
        history: generateHistory(15, 0, 1, isBullish ? 'up' : 'down')
      },
      gexCluster: {
        id: 'gex',
        label: 'Support Level',
        value: '+2.4Bn',
        verdict: "Strong Gamma Floor"
      },
      eventRadar: {
        id: 'event',
        label: 'Next Event',
        value: 'RBI Policy',
        verdict: "45m to Impact"
      },
      trafficLight: {
        id: 'traffic',
        label: 'System Status',
        value: 'GO',
        verdict: "Long Signals Active"
      },
      fomoMeter: {
        id: 'fomo',
        label: 'Greed Meter',
        value: 85,
        verdict: "Extreme Greed (Wait)"
      }
    }
  };
};

export const getHelpContent = (id: string): { title: string; description: string; rule: string } => {
  const helpMap: Record<string, { title: string; description: string; rule: string }> = {
    kelly: {
      title: 'POSITION SIZING (KELLY)',
      description: 'Calculates the mathematically optimal percentage of your capital to allocate based on current win probability and risk/reward ratio. Regime-adjusted for market conditions.',
      rule: 'If > 15%, high-probability edge detected. If < 5%, stay small and preserve capital.'
    },
    regime: {
      title: 'MARKET REGIME (HMM)',
      description: 'Hidden Markov Model detects current market state: TRENDING (momentum works), MEAN-REVERTING (contrarian works), or CHAOTIC (stay away).',
      rule: 'Trade WITH the regime. Avoid counter-trend trades in TRENDING, avoid breakout trades in CHAOTIC.'
    },
    traffic: {
      title: 'TRADE TRAFFIC LIGHT',
      description: 'Weighted score (0-100) combining regime, VIX, and momentum. GO (>70), WAIT (40-70), STOP (<40).',
      rule: 'GREEN = favorable conditions. YELLOW = reduce size. RED = avoid new trades.'
    },
    fomo: {
      title: 'FOMO METER',
      description: 'Measures market emotion using RSI + Bollinger Bands + Volume confirmation. Prevents buying at tops or selling at bottoms.',
      rule: 'EXTREME GREED (>75) = wait for pullback. EXTREME FEAR (<25) = look for reversal.'
    },
    streak: {
      title: 'STREAK REVERSAL (RF)',
      description: 'Random Forest model predicts probability of streak reversal. Confidence adjusted for rare long streaks.',
      rule: 'High reversal probability after 4+ consecutive days = potential reversal zone.'
    }
  };

  return helpMap[id] || {
    title: id.toUpperCase().replace(/_/g, ' '),
    description: "Statistical analysis of market conditions using institutional-grade formulas.",
    rule: "Consult multiple tiles for confluence before making trading decisions."
  };
};