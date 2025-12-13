export type TrendDirection = 'up' | 'down' | 'neutral';
export type Sentiment = 'bullish' | 'bearish' | 'neutral' | 'extreme_greed' | 'extreme_fear';

export interface DataPoint {
  id: string;
  label: string;
  value: string | number;
  unit?: string;
  change?: number; // percentage or value change
  trend?: TrendDirection;
  verdict: string; // The one-liner summary
  history?: { value: number; time: string }[]; // For charts
  meta?: any; // For specialized data like lists or heatmaps
}

export interface MarketDataState {
  indexName: 'NIFTY' | 'BANKNIFTY';
  timestamp: string;
  hero: {
    verdictTitle: string;
    verdictSubtitle: string;
    bullishProbability: number; // 0-100
    riskLevel: number; // 0-100
    riskVerdict: string; // NEW
    kellySize: number; // percentage
    kellyVerdict: string; // NEW
  };
  tiles: {
    // Row 1
    spotPrice: DataPoint;
    indiaVix: DataPoint;
    probabilitySurface: DataPoint;
    regimeBeacon: DataPoint;
    kellyOptimal: DataPoint;
    // Row 2
    varGauge: DataPoint;
    hurstCompass: DataPoint;
    vixTerm: DataPoint;
    fridayFear: DataPoint;
    thetaDecay: DataPoint;
    // Row 3
    monteCarlo: DataPoint;
    barrierBreach: DataPoint;
    streakReversal: DataPoint;
    painZone: DataPoint;
    rangeQuartiles: DataPoint;
    // Row 4
    momentumPulse: DataPoint;
    gexCluster: DataPoint;
    eventRadar: DataPoint;
    trafficLight: DataPoint;
    fomoMeter: DataPoint;
  };
  overallVerdict?: {
    stance: string;
    action: string;
    strategy: string;
    summary: string;
    bullishSignals: number;
    bearishSignals: number;
    totalSignals: number;
    bullishPct: number;
    kellySize: string;
    disclaimer: string;
  };
  forecast?: {
    tomorrow: string;
    intraday: string;
    swing: string;
  };
}

export interface TileHelpContent {
  title: string;
  description: string;
  decisionRule: string;
}