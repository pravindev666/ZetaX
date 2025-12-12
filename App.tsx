import React, { useState, useEffect } from 'react';
import { RefreshCw, Maximize2, Info, Moon, Sun, AlertTriangle, Radio, Shield, FileText, Lock, HelpCircle } from 'lucide-react';
import { getMarketData, getHelpContent, getMarketDataAsync } from './services/marketData';
import { MarketDataState, DataPoint } from './types';
import { GlassTile, Modal, SegmentedControl, StatusDot } from './components/ui';
import { MiniSparkline, MiniBarChart, TermStructureChart, CyberRadialGauge, HeatmapStrip, CyberReactor, CyberCompass, CyberBeacon, CyberRadar, CyberReticle, CyberRangeBar } from './components/charts';

// --- Helper to determine color based on verdict/value ---
const getAccent = (dp: DataPoint): 'bullish' | 'bearish' | 'neutral' | 'warning' => {
  const v = dp.verdict.toLowerCase();
  if (v.includes('bull') || v.includes('up') || v.includes('safe') || v.includes('green') || v.includes('call')) return 'bullish';
  if (v.includes('bear') || v.includes('risk') || v.includes('down') || v.includes('fear') || v.includes('put')) return 'bearish';
  if (v.includes('wait') || v.includes('chop') || v.includes('warn') || v.includes('wide')) return 'warning';
  return 'neutral';
};

// --- Empty Page View Component ---
const EmptyPage = ({ title, onBack }: { title: string, onBack: () => void }) => (
  <div className="min-h-screen pt-32 px-8 max-w-4xl mx-auto text-text-main">
    <button onClick={onBack} className="text-cyan-500 mb-8 hover:underline font-mono">← BACK TO DASHBOARD</button>
    <h1 className="text-4xl font-header font-bold mb-4">{title}</h1>
    <div className="h-px w-full bg-border mb-8"></div>
    <div className="p-12 border border-dashed border-border rounded-lg flex flex-col items-center justify-center opacity-50">
      <Lock size={48} className="mb-4 text-text-muted" />
      <p className="text-xl font-mono">CONTENT_LOCKED // COMING_SOON</p>
    </div>
  </div>
);

export default function App() {
  const [index, setIndex] = useState<'NIFTY' | 'BANKNIFTY'>('NIFTY');
  const [data, setData] = useState<MarketDataState | null>(null);
  const [helpModal, setHelpModal] = useState<{ isOpen: boolean; content: any }>({ isOpen: false, content: null });
  const [disclaimerOpen, setDisclaimerOpen] = useState(false);
  const [cookieConsentOpen, setCookieConsentOpen] = useState(false);
  const [isHowToOpen, setIsHowToOpen] = useState(false);
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [view, setView] = useState<string>('dashboard');

  // --- Initial Checks (Theme, Disclaimer, Cookies) ---
  useEffect(() => {
    // Theme Check
    const savedTheme = localStorage.getItem('rubix_theme') as 'dark' | 'light';
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.setAttribute('data-theme', savedTheme);
    }

    // Disclaimer Check (Every 48 Hours)
    const lastDisclaimer = localStorage.getItem('rubix_disclaimer_ack');
    if (!lastDisclaimer) {
      setDisclaimerOpen(true);
    } else {
      const lastTime = parseInt(lastDisclaimer, 10);
      const now = new Date().getTime();
      const hoursPassed = (now - lastTime) / (1000 * 60 * 60);
      if (hoursPassed > 48) {
        setDisclaimerOpen(true);
      }
    }

    // Cookie Check
    const cookieChoice = localStorage.getItem('rubix_cookie_consent');
    if (!cookieChoice) {
      setCookieConsentOpen(true);
    }
  }, []);

  // --- Theme Toggle ---
  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('rubix_theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  // --- Disclaimer Accept ---
  const acceptDisclaimer = () => {
    localStorage.setItem('rubix_disclaimer_ack', new Date().getTime().toString());
    setDisclaimerOpen(false);
  };

  // --- Cookie Actions ---
  const handleCookie = (action: string) => {
    localStorage.setItem('rubix_cookie_consent', action);
    setCookieConsentOpen(false);
  };

  // --- Fetch Data ---
  const refreshData = async () => {
    setData(null); // Loading state
    try {
      // Try to fetch live data from Python-generated JSON
      const liveData = await getMarketDataAsync(index);
      setData(liveData);
    } catch (error) {
      console.error('Error fetching data:', error);
      // Fallback to mock data
      setData(getMarketData(index));
    }
  };

  // --- Hard Refresh ---
  const hardRefresh = () => {
    window.location.reload();
  };

  useEffect(() => {
    refreshData();
  }, [index]);

  // --- Handlers ---
  const openHelp = (id: string) => {
    setHelpModal({
      isOpen: true,
      content: getHelpContent(id)
    });
  };

  // --- Render Empty Page ---
  if (view !== 'dashboard') {
    return <EmptyPage title={view} onBack={() => setView('dashboard')} />;
  }

  // --- Render Loading ---
  if (!data) return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-background">
      <div className="z-10 flex flex-col items-center gap-6">
        <div className="relative">
          <div className="w-16 h-16 border-t-2 border-l-2 border-cyan-500 rounded-full animate-spin"></div>
          <div className="w-16 h-16 border-b-2 border-r-2 border-green-500 rounded-full animate-spin absolute top-0 left-0" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
        </div>
        <p className="text-cyan-500 font-header text-xl tracking-[0.3em] uppercase animate-pulse">Initializing Core</p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen font-sans selection:bg-cyan-500/30 pb-20 relative transition-colors duration-300">

      {/* --- Disclaimer Modal --- */}
      <Modal
        isOpen={disclaimerOpen}
        title="Protocol Alpha"
        preventClose={true}
      >
        <div className="space-y-6">
          <div className="flex items-center gap-4 text-warning border-b border-warning/20 pb-4">
            <AlertTriangle size={32} />
            <h3 className="font-bold text-xl font-header tracking-wide">RESTRICTED ENVIRONMENT</h3>
          </div>
          <p className="text-lg leading-relaxed text-text-main">
            You are entering the <strong>Tradyxa RubiX</strong> probabilistic interface.
            <br /><br />
            <span className="text-red-400">WARNING:</span> This system provides raw statistical data for professional traders. It is NOT financial advice.
          </p>
          <button
            onClick={acceptDisclaimer}
            className="w-full bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500 text-cyan-600 dark:text-cyan-400 hover:text-text-main py-4 rounded-sm font-header font-bold text-lg uppercase tracking-widest transition-all mt-4 hover:shadow-[0_0_20px_rgba(0,243,255,0.4)]"
          >
            I Understand & Enter
          </button>
        </div>
      </Modal>

      {/* --- Help Modal --- */}
      <Modal
        isOpen={helpModal.isOpen}
        onClose={() => setHelpModal({ ...helpModal, isOpen: false })}
        title={helpModal.content?.title || 'System'}
      >
        <p className="mb-6 text-text-main text-lg">{helpModal.content?.description}</p>
        <div className="bg-background p-4 border-l-4 border-cyan-500 shadow-lg">
          <span className="text-sm text-cyan-500 font-header font-bold tracking-widest block mb-2">DECISION PROTOCOL</span>
          <p className="text-lg font-mono text-text-main leading-relaxed">{helpModal.content?.rule}</p>
        </div>
      </Modal>

      {/* --- Cookie Consent Overlay --- */}
      {cookieConsentOpen && (
        <div className="fixed bottom-0 left-0 w-full z-50 bg-surface border-t border-cyan-500/30 p-6 shadow-[0_-10px_40px_rgba(0,0,0,0.5)] animate-in slide-in-from-bottom-10 fade-in duration-500">
          <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div className="max-w-3xl">
              <h3 className="text-lg font-header font-bold text-text-main mb-2 flex items-center gap-2">
                <Shield size={18} className="text-cyan-500" /> Cookies & Advertising Consent
              </h3>
              <p className="text-sm text-text-muted leading-relaxed">
                We use cookies for theme preferences and performance. Our advertising partner (Adsterra) may also use cookies to show you relevant ads. You can control this below.
              </p>
              <div className="flex gap-4 mt-2 text-xs text-cyan-600 dark:text-cyan-400 font-mono">
                <span>Privacy</span> <span>·</span> <span>Cookies</span> <span>·</span> <span>Terms</span>
              </div>
            </div>
            <div className="flex flex-wrap gap-3">
              <button onClick={() => handleCookie('allow_all')} className="bg-cyan-600 hover:bg-cyan-500 text-white px-6 py-2 rounded-sm font-bold text-sm transition-colors">Accept all</button>
              <button onClick={() => handleCookie('reject_all')} className="bg-surface border border-border text-text-muted hover:text-text-main px-6 py-2 rounded-sm font-bold text-sm transition-colors">Reject all</button>
              <button onClick={() => handleCookie('save')} className="text-cyan-600 dark:text-cyan-400 hover:underline px-4 py-2 text-sm">Save choices</button>
            </div>
          </div>
        </div>
      )}

      {/* --- Main Layout --- */}
      <div className="max-w-[1800px] mx-auto p-4 md:p-8 flex flex-col gap-8 relative z-10">

        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-center bg-surface/80 backdrop-blur-md p-6 border border-border rounded-sm gap-6 shadow-sm">
          <div className="flex items-center gap-6">
            <div className="w-12 h-12 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-sm flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Radio className="text-white" size={24} />
            </div>
            <div>
              <h1 className="text-4xl font-header font-black tracking-tight text-text-main leading-none">
                TRADYXA <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">RUBIX</span>
              </h1>
              <div className="flex items-center gap-2 mt-1">
                <div className="h-1 w-20 bg-gray-700 rounded-full overflow-hidden">
                  <div className="h-full bg-green-500 animate-[width_2s_ease-in-out_infinite]" style={{ width: '60%' }}></div>
                </div>
                <span className="text-[10px] text-text-muted font-mono tracking-widest uppercase">Live Connection</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden xl:block text-right mr-4">
              <div className="text-xs text-text-muted font-mono uppercase">Last Sync</div>
              <div className="text-xl font-mono text-cyan-600 dark:text-cyan-400">{data.timestamp}</div>
            </div>

            <SegmentedControl
              options={['NIFTY', 'BANKNIFTY']}
              selected={index}
              onChange={(v) => setIndex(v as any)}
            />

            <button
              onClick={toggleTheme}
              className="p-3 bg-surface hover:bg-border/50 border border-border hover:border-cyan-500 rounded-sm text-text-muted transition-all duration-300"
              title="Toggle Theme"
            >
              {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            </button>

            <button
              onClick={hardRefresh}
              className="p-3 bg-surface hover:bg-border/50 border border-border hover:border-cyan-500 rounded-sm text-text-muted transition-all duration-300 group"
              title="Hard Refresh"
            >
              <RefreshCw size={20} className="group-hover:rotate-180 transition-transform duration-500" />
            </button>
          </div>
        </header>

        {/* Hero Section - The Verdict */}
        <section className="grid grid-cols-1 xl:grid-cols-4 gap-6">
          {/* Main Verdict Tile */}
          <div className="xl:col-span-2 bg-gradient-to-r from-surface to-background border border-border p-8 rounded-sm relative overflow-hidden group hover:border-cyan-500/50 transition-colors shadow-lg">
            <div className="absolute top-0 right-0 p-4 opacity-5 dark:opacity-10 pointer-events-none">
              <Radio size={120} className="text-text-main" />
            </div>
            <div className="relative z-10">
              <h2 className="text-sm font-mono text-cyan-600 dark:text-cyan-400 font-bold uppercase tracking-[0.2em] mb-3">AI Consensus</h2>
              <div className="text-4xl md:text-5xl font-header font-black text-text-main mb-4 leading-tight shadow-black drop-shadow-xl">
                {data.hero.verdictTitle}
              </div>
              <p className="text-xl text-text-muted font-light border-l-4 border-bullish pl-4 leading-relaxed max-w-2xl">
                {data.hero.verdictSubtitle}
              </p>
            </div>
          </div>

          {/* Stats Cluster */}
          <div className="xl:col-span-1 bg-surface/80 backdrop-blur-md border border-border p-6 rounded-sm flex flex-col justify-center items-center relative">
            <h3 className="absolute top-4 left-4 text-xs font-mono text-text-muted uppercase tracking-widest">Bull Probability</h3>
            <div className="w-full h-40">
              <CyberRadialGauge value={data.hero.bullishProbability} color="#00ff9d" label="Confidence" isLight={theme === 'light'} />
            </div>
          </div>

          <div className="xl:col-span-1 flex flex-col gap-4">
            {/* Risk Module */}
            <div className="flex-1 bg-surface/80 border border-border p-5 rounded-sm flex flex-col justify-between group">
              <div>
                <div className="flex justify-between items-end mb-2">
                  <span className="text-xs font-mono text-text-muted tracking-widest uppercase">Market Risk</span>
                  <span className={`text-2xl font-mono font-bold ${data.hero.riskLevel > 50 ? 'text-bearish' : 'text-bullish'}`}>{data.hero.riskLevel}%</span>
                </div>
                <div className="w-full h-2 bg-background rounded-sm overflow-hidden">
                  <div
                    className={`h-full ${data.hero.riskLevel > 50 ? 'bg-bearish shadow-[0_0_10px_rgba(255,51,51,0.5)]' : 'bg-bullish shadow-[0_0_10px_rgba(0,255,157,0.5)]'} transition-all duration-1000`}
                    style={{ width: `${data.hero.riskLevel}%` }}
                  />
                </div>
              </div>
              <div className="mt-3 text-[10px] font-mono font-bold uppercase text-text-muted group-hover:text-text-main transition-colors">
                VERDICT: <span className={data.hero.riskLevel > 50 ? 'text-bearish' : 'text-bullish'}>{data.hero.riskVerdict}</span>
              </div>
            </div>

            {/* Kelly Module */}
            <div className="flex-1 bg-surface/80 border border-border p-5 rounded-sm flex flex-col justify-between group">
              <div>
                <div className="flex justify-between items-end mb-2">
                  <span className="text-xs font-mono text-text-muted tracking-widest uppercase">System Size</span>
                  <span className="text-2xl font-mono font-bold text-cyan-600 dark:text-cyan-400">{data.hero.kellySize}%</span>
                </div>
                <div className="w-full h-2 bg-background rounded-sm overflow-hidden">
                  <div
                    className="h-full bg-cyan-400 shadow-[0_0_10px_rgba(0,243,255,0.5)] transition-all duration-1000"
                    style={{ width: `${data.hero.kellySize}%` }}
                  />
                </div>
              </div>
              <div className="mt-3 text-[10px] font-mono font-bold uppercase text-text-muted group-hover:text-text-main transition-colors">
                VERDICT: <span className="text-cyan-600 dark:text-cyan-400">{data.hero.kellyVerdict}</span>
              </div>
            </div>
          </div>
        </section>

        {/* 
            THE GRID 
        */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-6">

          {/* --- Row 1 --- */}
          <GlassTile title={data.tiles.spotPrice.label} verdict={data.tiles.spotPrice.verdict} onHelp={() => openHelp('spot')} accent={getAccent(data.tiles.spotPrice)}>
            <div className="text-4xl font-mono font-bold text-text-main tracking-tighter drop-shadow-lg">{Number(data.tiles.spotPrice.value).toLocaleString('en-IN', { maximumFractionDigits: 0 })}</div>
            <div className={`text-lg font-bold mt-1 ${data.tiles.spotPrice.change! > 0 ? 'text-bullish' : 'text-bearish'}`}>
              {data.tiles.spotPrice.change! > 0 ? '▲' : '▼'} {Math.abs(data.tiles.spotPrice.change!)}%
            </div>
            <MiniSparkline data={data.tiles.spotPrice.history!} color={data.tiles.spotPrice.trend === 'up' ? '#00ff9d' : '#ff3333'} isLight={theme === 'light'} />
          </GlassTile>

          <GlassTile title={data.tiles.indiaVix.label} verdict={data.tiles.indiaVix.verdict} onHelp={() => openHelp('vix')} accent={getAccent(data.tiles.indiaVix)}>
            <div className="text-4xl font-mono text-text-main font-bold">{data.tiles.indiaVix.value}</div>
            <div className="text-sm text-text-muted mt-1">Implied Volatility</div>
            <MiniSparkline data={data.tiles.indiaVix.history!} color="#ff3333" isLight={theme === 'light'} />
          </GlassTile>

          <GlassTile title={data.tiles.hurstCompass.label} verdict={data.tiles.hurstCompass.verdict} onHelp={() => openHelp('hurst')} accent={getAccent(data.tiles.hurstCompass)}>
            <CyberCompass value={Number(data.tiles.hurstCompass.value)} isLight={theme === 'light'} />
          </GlassTile>

          <GlassTile title={data.tiles.momentumPulse.label} verdict={data.tiles.momentumPulse.verdict} onHelp={() => openHelp('momentum')} accent={getAccent(data.tiles.momentumPulse)}>
            <div className={`text-3xl font-mono font-bold drop-shadow-md ${data.tiles.momentumPulse.trend === 'up' ? 'text-bullish' : 'text-bearish'}`}>{data.tiles.momentumPulse.value}</div>
            <div className="text-xs text-text-muted mb-2">Velocity Score</div>
            <MiniSparkline data={data.tiles.momentumPulse.history!} color={data.tiles.momentumPulse.trend === 'up' ? '#00ff9d' : '#ff3333'} isLight={theme === 'light'} />
          </GlassTile>

          {/* --- Row 2 --- */}
          <GlassTile title={data.tiles.regimeBeacon.label} verdict={data.tiles.regimeBeacon.verdict} onHelp={() => openHelp('regime')} accent={getAccent(data.tiles.regimeBeacon)}>
            <CyberBeacon value={String(data.tiles.regimeBeacon.value)} isLight={theme === 'light'} />
          </GlassTile>

          <GlassTile title={data.tiles.varGauge.label} verdict={data.tiles.varGauge.verdict} onHelp={() => openHelp('var')} accent="bearish">
            <div className="text-4xl font-mono text-text-main">{data.tiles.varGauge.value}</div>
            <div className="text-xs text-red-400 mt-2 font-bold uppercase tracking-wider">Warning Level: 95% Conf</div>
          </GlassTile>

          <GlassTile title={data.tiles.vixTerm.label} verdict={data.tiles.vixTerm.verdict} onHelp={() => openHelp('vixterm')} accent="neutral">
            <TermStructureChart data={data.tiles.vixTerm.history!} isLight={theme === 'light'} />
            <div className="text-center text-xs text-cyan-600 dark:text-cyan-400 mt-2 font-mono">TERM STRUCTURE: {data.tiles.vixTerm.value.toUpperCase()}</div>
          </GlassTile>

          <GlassTile title={data.tiles.fridayFear.label} verdict={data.tiles.fridayFear.verdict} onHelp={() => openHelp('fear')} accent={getAccent(data.tiles.fridayFear)}>
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="text-3xl font-header font-bold text-text-main tracking-widest">{data.tiles.fridayFear.value}</div>
                <div className="text-[10px] text-text-muted uppercase mt-1">Carry Risk</div>
              </div>
            </div>
          </GlassTile>

          {/* --- Row 3 --- */}
          <GlassTile title={data.tiles.painZone.label} verdict={data.tiles.painZone.verdict} onHelp={() => openHelp('pain')} accent="neutral">
            <CyberReticle value={Number(data.tiles.painZone.value)} label="Highest OI Strike" isLight={theme === 'light'} />
          </GlassTile>

          <GlassTile title={data.tiles.gexCluster.label} verdict={data.tiles.gexCluster.verdict} onHelp={() => openHelp('gex')} accent="bullish">
            <div className="text-3xl font-mono text-text-main">{data.tiles.gexCluster.value}</div>
            <div className="w-full h-2 bg-background mt-3 rounded-sm">
              <div className="h-full bg-bullish w-[70%] shadow-[0_0_10px_rgba(0,255,157,0.3)]"></div>
            </div>
          </GlassTile>

          <GlassTile title={data.tiles.probabilitySurface.label} verdict={data.tiles.probabilitySurface.verdict} onHelp={() => openHelp('probs')} accent="neutral">
            <div className="text-2xl font-header font-bold text-cyan-600 dark:text-neutral tracking-wide">{data.tiles.probabilitySurface.value.toUpperCase()}</div>
            <HeatmapStrip value="neutral" />
          </GlassTile>

          <GlassTile title={data.tiles.thetaDecay.label} verdict={data.tiles.thetaDecay.verdict} onHelp={() => openHelp('theta')} accent="neutral">
            <div className="text-3xl font-mono text-cyan-600 dark:text-neutral font-bold">{data.tiles.thetaDecay.value}</div>
            <div className="text-sm text-text-muted font-mono text-right">{data.tiles.thetaDecay.unit}</div>
          </GlassTile>

          {/* --- Row 4 --- */}
          <GlassTile title={data.tiles.kellyOptimal.label} verdict={data.tiles.kellyOptimal.verdict} onHelp={() => openHelp('kelly')} accent={getAccent(data.tiles.kellyOptimal)}>
            <div className="flex items-center justify-center h-full gap-4">
              <span className="text-5xl font-mono font-black text-cyan-600 dark:text-cyan-400 drop-shadow-[0_0_10px_rgba(0,243,255,0.4)]">{data.tiles.kellyOptimal.value}</span>
            </div>
          </GlassTile>

          <GlassTile title={data.tiles.barrierBreach.label} verdict={data.tiles.barrierBreach.verdict} onHelp={() => openHelp('barrier')} accent="warning">
            <div className="text-4xl font-mono text-warning font-bold">{data.tiles.barrierBreach.value}</div>
          </GlassTile>

          <GlassTile title={data.tiles.trafficLight.label} verdict={data.tiles.trafficLight.verdict} onHelp={() => openHelp('traffic')} accent="bullish">
            <div className="w-full h-full p-2 flex items-center justify-center">
              <CyberReactor status={String(data.tiles.trafficLight.value)} isLight={theme === 'light'} />
            </div>
          </GlassTile>

          <GlassTile title={data.tiles.fomoMeter.label} verdict={data.tiles.fomoMeter.verdict} onHelp={() => openHelp('fomo')} accent="bearish">
            <div className="w-full h-full p-2 flex items-center justify-center">
              <div className="w-32 h-32">
                <CyberRadialGauge value={Number(data.tiles.fomoMeter.value)} color="#ff3333" isLight={theme === 'light'} />
              </div>
            </div>
          </GlassTile>

          {/* --- Row 5 --- */}
          <GlassTile title={data.tiles.eventRadar.label} verdict={data.tiles.eventRadar.verdict} onHelp={() => openHelp('event')} accent="warning">
            <CyberRadar event={String(data.tiles.eventRadar.value)} time={data.tiles.eventRadar.verdict} isLight={theme === 'light'} />
          </GlassTile>

          <GlassTile title={data.tiles.rangeQuartiles.label} verdict={data.tiles.rangeQuartiles.verdict} onHelp={() => openHelp('range')} accent="neutral">
            <CyberRangeBar range={String(data.tiles.rangeQuartiles.value)} isLight={theme === 'light'} />
          </GlassTile>

        </div>

        {/* How To Use (Collapsible) */}
        <div
          onClick={() => setIsHowToOpen(!isHowToOpen)}
          className="group border border-border bg-surface/80 p-4 flex flex-col cursor-pointer hover:border-cyan-500/30 transition-all rounded-sm relative overflow-hidden"
        >
          <div className="absolute top-0 left-0 w-1 h-full bg-cyan-500 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-cyan-500/10 p-2 rounded-full">
                <Info size={20} className="text-cyan-600 dark:text-cyan-400" />
              </div>
              <span className="text-sm font-header font-bold text-cyan-600 dark:text-cyan-400 uppercase tracking-widest">HOW TO USE THIS DASHBOARD</span>
            </div>
            <span className="text-text-muted text-xs font-mono">{isHowToOpen ? 'COLLAPSE [-]' : 'EXPAND [+]'}</span>
          </div>

          {isHowToOpen && (
            <div className="mt-6 space-y-6 text-sm text-text-muted border-t border-border pt-6 animate-in fade-in slide-in-from-top-4">

              {/* Simple 3-Step Guide */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-background border border-border p-4 rounded-sm">
                  <div className="text-2xl font-bold text-bullish mb-2">1️⃣</div>
                  <strong className="text-text-main block mb-1">Check System Status</strong>
                  <p className="text-xs">Look for <span className="text-bullish font-bold">GO</span> = trade, <span className="text-warning font-bold">WAIT</span> = be careful, <span className="text-bearish font-bold">STOP</span> = avoid trading.</p>
                </div>
                <div className="bg-background border border-border p-4 rounded-sm">
                  <div className="text-2xl font-bold text-neutral mb-2">2️⃣</div>
                  <strong className="text-text-main block mb-1">Read the Verdicts</strong>
                  <p className="text-xs">Every tile has a <span className="text-cyan-500 font-bold">VERDICT</span> at the bottom. This is your simple, plain-English answer. Trust it.</p>
                </div>
                <div className="bg-background border border-border p-4 rounded-sm">
                  <div className="text-2xl font-bold text-magenta mb-2">3️⃣</div>
                  <strong className="text-text-main block mb-1">Follow Bet Size</strong>
                  <p className="text-xs">The <span className="text-cyan-500 font-bold">Bet Size</span> tile tells you exactly how much to invest. If it says 5%, only use 5% of your capital.</p>
                </div>
              </div>

              {/* What Each Verdict Means */}
              <div className="bg-surface border border-border p-4 rounded-sm">
                <strong className="text-cyan-500 block mb-3 font-header text-lg">🎯 WHAT THE VERDICTS MEAN (Plain English)</strong>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div><span className="text-text-main font-bold">TRENDING</span> = Market has momentum. Trade with the direction.</div>
                  <div><span className="text-text-main font-bold">MEAN-REVERTING</span> = Market bounces back. Trade the opposite.</div>
                  <div><span className="text-text-main font-bold">SELL PREMIUM</span> = Option sellers have advantage today.</div>
                  <div><span className="text-text-main font-bold">BUYER WINDOW</span> = Good time to buy options.</div>
                  <div><span className="text-text-main font-bold">MAGNET: 26000</span> = Price will likely stick around 26000 at expiry.</div>
                  <div><span className="text-text-main font-bold">WEAK SUPPORT</span> = Careful! No strong floor below.</div>
                  <div><span className="text-text-main font-bold">CONSERVATIVE</span> = Go small. Market is unpredictable.</div>
                  <div><span className="text-text-main font-bold">GREED METER HIGH</span> = Everyone is buying. Maybe wait for dip.</div>
                </div>
              </div>

              {/* Quick Color Reference */}
              <div className="flex flex-wrap gap-4 text-xs">
                <div className="flex items-center gap-2"><div className="w-3 h-3 bg-bullish rounded-full"></div><span><span className="text-bullish font-bold">GREEN</span> = Bullish / Safe</span></div>
                <div className="flex items-center gap-2"><div className="w-3 h-3 bg-bearish rounded-full"></div><span><span className="text-bearish font-bold">RED</span> = Bearish / Risky</span></div>
                <div className="flex items-center gap-2"><div className="w-3 h-3 bg-neutral rounded-full"></div><span><span className="text-neutral font-bold">CYAN</span> = Neutral Info</span></div>
                <div className="flex items-center gap-2"><div className="w-3 h-3 bg-warning rounded-full"></div><span><span className="text-warning font-bold">YELLOW</span> = Caution</span></div>
              </div>

            </div>
          )}
        </div>

        {/* Overall Verdict - ML Summary */}
        {data.overallVerdict && (
          <div className="bg-surface/90 backdrop-blur-sm border border-border rounded-sm p-6 mt-6 relative overflow-hidden group hover:border-cyan-500/50 transition-colors shadow-lg max-w-3xl mx-auto">
            {/* Accent bar at top */}
            <div className={`absolute top-0 left-0 right-0 h-1 ${data.overallVerdict.stance === 'BULLISH' || data.overallVerdict.stance === 'LEAN BULLISH'
                ? 'bg-bullish'
                : data.overallVerdict.stance === 'BEARISH' || data.overallVerdict.stance === 'LEAN BEARISH'
                  ? 'bg-bearish'
                  : 'bg-neutral'
              }`}></div>

            <div className="text-center">
              <h3 className="text-sm font-mono text-text-muted uppercase tracking-widest mb-2">{data.indexName} Analysis</h3>
              <div className={`text-4xl font-header font-black mb-2 ${data.overallVerdict.stance.includes('BULLISH')
                  ? 'text-bullish'
                  : data.overallVerdict.stance.includes('BEARISH')
                    ? 'text-bearish'
                    : 'text-neutral'
                }`}>
                {data.overallVerdict.stance}
              </div>
              <p className="text-lg text-text-main font-medium mb-4">{data.overallVerdict.action}</p>

              {/* Signal breakdown */}
              <div className="flex justify-center gap-6 mb-4 text-sm">
                <div className="text-bullish">
                  <span className="font-bold text-2xl">{data.overallVerdict.bullishSignals}</span>
                  <div className="text-xs opacity-75">Bullish</div>
                </div>
                <div className="text-text-muted">
                  <span className="font-bold text-2xl">{data.overallVerdict.totalSignals}</span>
                  <div className="text-xs opacity-75">Total</div>
                </div>
                <div className="text-bearish">
                  <span className="font-bold text-2xl">{data.overallVerdict.bearishSignals}</span>
                  <div className="text-xs opacity-75">Bearish</div>
                </div>
              </div>

              {/* Strategy */}
              <div className="bg-background p-4 rounded-sm border-l-4 border-cyan-500 text-left mb-4">
                <span className="text-xs text-cyan-500 font-mono uppercase tracking-wider">Suggested Strategy</span>
                <p className="text-text-main font-medium mt-1">{data.overallVerdict.strategy}</p>
              </div>

              {/* Kelly reminder */}
              <div className="text-sm text-text-muted mb-4">
                Position Size: <span className="text-cyan-500 font-bold">{data.overallVerdict.kellySize}</span> of capital per trade
              </div>

              {/* Disclaimer */}
              <p className="text-[10px] text-text-muted opacity-60 border-t border-border pt-3">
                {data.overallVerdict.disclaimer}
              </p>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="text-xs text-text-muted font-mono py-8 border-t border-border mt-8 flex flex-col gap-6">
          <div className="flex flex-col md:flex-row justify-between gap-6">
            <div className="max-w-2xl">
              <p className="font-bold text-text-main mb-2">Data Sources: NSE India, Yahoo Finance</p>
              <p className="mb-1">Analytics powered by Tradyxa Analytics Engine v1.0.0</p>
              <p className="mb-1">Market data © respective owners. Tradyxa Quant Dashboard is unaffiliated with NSE or Yahoo.</p>
              <p>Market data may be delayed up to 30 minutes. For educational use only.</p>
            </div>
            <div className="max-w-md text-left md:text-right">
              <p className="font-bold text-text-main mb-2">Operated by Zeta Aztra Technologies (Individual Proprietorship, India)</p>
              <p>© 2025 Zeta Aztra Technologies. All Rights Reserved.</p>
              <p className="mt-1">zetaaztratech@gmail.com | Jurisdiction: Chennai, Tamil Nadu | Version: v1.0.0</p>
            </div>
          </div>

          <div className="border-t border-border pt-6">
            <p className="mb-4 text-[10px] opacity-70">
              Visual models and code protected under Copyright Act, 1957 (India). Unauthorized use of the Tradyxa or Zeta Aztra name, logo, or visuals is strictly prohibited.
              Tradyxa Quant Dashboard is a product of Zeta Aztra Technologies (India) and is not affiliated with any other Tradyxa-named companies or domains.
            </p>
            <div className="flex flex-wrap gap-2 text-cyan-600 dark:text-cyan-400 font-bold">
              <button onClick={() => setView('Privacy Policy')} className="hover:underline">Privacy Policy</button>
              <span>·</span>
              <button onClick={() => setView('Cookie Preferences')} className="hover:underline">Cookie Preferences</button>
              <span>·</span>
              <button onClick={() => setView('Terms of Use')} className="hover:underline">Terms of Use</button>
              <span>·</span>
              <button onClick={() => setView('Disclaimer')} className="hover:underline">Disclaimer</button>
              <span>·</span>
              <button onClick={() => setView('About')} className="hover:underline">About</button>
            </div>
          </div>
        </footer>

      </div>
    </div>
  );
}