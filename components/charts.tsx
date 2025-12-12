import React from 'react';
import { AreaChart, Area, LineChart, Line, BarChart, Bar, ResponsiveContainer, XAxis, YAxis, Tooltip, PieChart, Pie, Cell } from 'recharts';

// --- Theme Helper ---
// Since Recharts needs JS hex values (can't read CSS vars easily inside SVG), 
// we pass the theme mode to components or assume a default.
export const getChartTheme = (isLight: boolean) => ({
  grid: isLight ? '#e2e8f0' : '#1a1a2e',
  text: isLight ? '#64748b' : '#64748b',
  bullish: '#00ff9d',
  bearish: '#ff3333',
  neutral: '#00f3ff',
  background: isLight ? '#ffffff' : '#0a0a12',
});

// --- Sparkline (Area) ---
export const MiniSparkline: React.FC<{ data: any[], color?: string, isLight?: boolean }> = ({ data, color, isLight = false }) => {
  const theme = getChartTheme(isLight);
  const finalColor = color || theme.bullish;
  
  return (
    <div className="h-16 w-full mt-2">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id={`grad-${finalColor.replace('#','')}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={finalColor} stopOpacity={0.4}/>
              <stop offset="95%" stopColor={finalColor} stopOpacity={0}/>
            </linearGradient>
          </defs>
          <Area 
            type="monotone" 
            dataKey="value" 
            stroke={finalColor} 
            strokeWidth={2} 
            fill={`url(#grad-${finalColor.replace('#','')})`} 
            isAnimationActive={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

// --- Tiny Bar Chart ---
export const MiniBarChart: React.FC<{ data: any[], isLight?: boolean }> = ({ data, isLight = false }) => {
  const theme = getChartTheme(isLight);
  return (
    <div className="h-16 w-full mt-2">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <Bar dataKey="value" fill={theme.neutral} radius={[2, 2, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

// --- Term Structure Line ---
export const TermStructureChart: React.FC<{ data: any[], isLight?: boolean }> = ({ data, isLight = false }) => {
  const theme = getChartTheme(isLight);
  return (
    <div className="h-20 w-full mt-1">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <Line 
              type="monotone" 
              dataKey="value" 
              stroke={theme.neutral} 
              strokeWidth={3} 
              dot={{ r: 4, fill: theme.background, stroke: theme.neutral, strokeWidth: 2 }} 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

// --- Cyber Radial Gauge ---
export const CyberRadialGauge: React.FC<{ value: number, color: string, label?: string, isLight?: boolean }> = ({ value, color, label, isLight = false }) => {
  const theme = getChartTheme(isLight);
  const size = 100;
  const strokeWidth = 8;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <svg 
        viewBox={`0 0 ${size} ${size}`} 
        className="w-full h-full transform -rotate-90 max-h-[160px] max-w-[160px]"
        style={{ overflow: 'visible' }}
      >
        <circle cx={size / 2} cy={size / 2} r={radius} fill="transparent" stroke={theme.grid} strokeWidth={strokeWidth} strokeDasharray="4 2" />
        <defs>
          <filter id={`glow-${color.replace('#', '')}`}>
            <feGaussianBlur stdDeviation="2" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="transparent"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          filter={`url(#glow-${color.replace('#', '')})`}
          className="transition-all duration-1000 ease-out"
        />
        <circle cx={size / 2} cy={size / 2} r={radius - 12} fill="transparent" stroke={color} strokeWidth="0.5" opacity="0.5" />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className={`text-3xl font-mono font-bold ${isLight ? 'text-gray-900' : 'text-white'} drop-shadow-md tracking-tighter`}>{value}%</span>
        {label && <span className="text-[9px] font-header font-bold text-gray-500 uppercase tracking-widest mt-1">{label}</span>}
      </div>
    </div>
  );
};

// --- Cyber Reactor ---
export const CyberReactor: React.FC<{ status: string, isLight?: boolean }> = ({ status, isLight = false }) => {
  const isGo = status === 'GO';
  const isWait = status === 'WAIT';
  const color = isGo ? '#00ff9d' : isWait ? '#ffcc00' : '#ff3333';
  const gridColor = isLight ? '#cbd5e1' : '#1a1a2e';
  const bgColor = isLight ? '#ffffff' : '#0a0a12';
  
  return (
    <div className="w-full h-full flex items-center justify-center relative">
      <svg width="100%" height="100%" viewBox="0 0 100 100" className="max-h-[140px] max-w-[140px] overflow-visible">
        <defs>
          <filter id={`reactor-glow-${status}`} x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        <circle cx="50" cy="50" r="45" stroke={gridColor} strokeWidth="1" fill="none" />
        <path d="M 50 2 L 50 10 M 50 90 L 50 98 M 2 50 L 10 50 M 90 50 L 98 50" stroke={color} strokeWidth="1.5" opacity="0.6" />
        <g style={{ transformOrigin: 'center', animation: 'spin 10s linear infinite' }}>
          <circle cx="50" cy="50" r="38" stroke={color} strokeWidth="1" strokeDasharray="10 30" fill="none" opacity="0.4" />
          <circle cx="50" cy="50" r="41" stroke={color} strokeWidth="0.5" strokeDasharray="60 120" fill="none" opacity="0.3" />
        </g>
        <g style={{ transformOrigin: 'center', animation: 'spin 4s linear infinite reverse' }}>
          <circle cx="50" cy="50" r="30" stroke={color} strokeWidth="3" strokeDasharray="25 35" fill="none" filter={`url(#reactor-glow-${status})`} />
        </g>
        <circle cx="50" cy="50" r="20" fill={bgColor} stroke={color} strokeWidth="1" />
        <circle cx="50" cy="50" r="12" fill={color} fillOpacity="0.15" className="animate-pulse" />
        <text x="50" y="55" textAnchor="middle" fill={color} fontSize="16" fontWeight="bold" fontFamily="monospace" style={{ textShadow: `0 0 10px ${color}` }}>{status}</text>
      </svg>
      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
    </div>
  );
};

// --- Cyber Compass ---
export const CyberCompass: React.FC<{ value: number, isLight?: boolean }> = ({ value, isLight = false }) => {
  const theme = getChartTheme(isLight);
  const angle = (value - 0.5) * 180;
  const color = value > 0.6 ? theme.bullish : value < 0.4 ? theme.bearish : theme.neutral;

  return (
    <div className="w-full h-full flex flex-col items-center justify-end relative pb-2 overflow-hidden">
      <svg viewBox="0 0 200 110" className="w-full h-full overflow-visible">
        <defs>
          <linearGradient id="compass-grad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor={theme.bearish} stopOpacity="0.5"/>
            <stop offset="50%" stopColor={theme.neutral} stopOpacity="0.5"/>
            <stop offset="100%" stopColor={theme.bullish} stopOpacity="0.5"/>
          </linearGradient>
        </defs>
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke={theme.grid} strokeWidth="15" strokeLinecap="round" />
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="url(#compass-grad)" strokeWidth="4" strokeLinecap="round" strokeDasharray="1 4" />
        <line x1="100" y1="20" x2="100" y2="10" stroke={theme.neutral} strokeWidth="2" />
        <line x1="20" y1="100" x2="10" y2="100" stroke={theme.bearish} strokeWidth="2" />
        <line x1="180" y1="100" x2="190" y2="100" stroke={theme.bullish} strokeWidth="2" />
        <g style={{ transformOrigin: '100px 100px', transform: `rotate(${angle}deg)`, transition: 'transform 1.5s cubic-bezier(0.22, 1, 0.36, 1)' }}>
          <path d="M 100 100 L 100 25" stroke={color} strokeWidth="3" strokeLinecap="round" filter={`url(#glow-${color.replace('#','')})`} />
          <circle cx="100" cy="25" r="3" fill={color} />
          <circle cx="100" cy="100" r="8" fill={theme.background} stroke={color} strokeWidth="2" />
        </g>
        <text x="100" y="80" textAnchor="middle" fill={color} fontSize="14" fontFamily="monospace" fontWeight="bold">{value.toFixed(2)}</text>
      </svg>
      <div className="flex justify-between w-full px-4 text-[9px] text-gray-500 font-mono uppercase">
        <span>Mean Rev</span>
        <span>Trending</span>
      </div>
    </div>
  );
};

// --- Cyber Beacon ---
export const CyberBeacon: React.FC<{ value: string, isLight?: boolean }> = ({ value, isLight = false }) => {
  const theme = getChartTheme(isLight);
  return (
    <div className="w-full h-full flex items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 opacity-20" style={{ 
          backgroundImage: 'radial-gradient(circle, #00ff9d 1px, transparent 1px)', 
          backgroundSize: '20px 20px' 
      }}></div>
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-20 h-20 border border-bullish/30 rounded-full animate-[ping_3s_linear_infinite]" />
        <div className="w-32 h-32 border border-bullish/20 rounded-full animate-[ping_3s_linear_infinite]" style={{ animationDelay: '1s' }} />
        <div className="w-48 h-48 border border-bullish/10 rounded-full animate-[ping_3s_linear_infinite]" style={{ animationDelay: '2s' }} />
      </div>
      <div className={`relative z-10 flex flex-col items-center justify-center ${isLight ? 'bg-white/90' : 'bg-[#0a0a12]/80'} backdrop-blur-sm p-4 border border-bullish/50 rounded-sm shadow-[0_0_20px_rgba(0,255,157,0.2)]`}>
        <div className="w-3 h-3 bg-bullish rounded-full mb-2 animate-pulse shadow-[0_0_10px_#00ff9d]"></div>
        <span className="text-xl font-header font-bold text-bullish tracking-widest">{value}</span>
      </div>
    </div>
  );
};

// --- Cyber Radar (Animated) ---
export const CyberRadar: React.FC<{ event: string, time: string, isLight?: boolean }> = ({ event, time, isLight = false }) => {
  const theme = getChartTheme(isLight);
  const ringColor = isLight ? '#cbd5e1' : '#333';
  const textColor = isLight ? '#0f172a' : '#ffffff';

  return (
    <div className="w-full h-full flex flex-col justify-center items-center relative overflow-hidden px-2 py-2">
       {/* Compact Layout for Single Tile */}
       <div className="relative w-16 h-16 shrink-0 mb-2">
          <svg viewBox="0 0 100 100" className="w-full h-full">
             {/* Grid */}
             <circle cx="50" cy="50" r="48" stroke={ringColor} strokeWidth="1" fill={theme.background} />
             <circle cx="50" cy="50" r="30" stroke={ringColor} strokeWidth="1" fill="none" />
             <line x1="50" y1="2" x2="50" y2="98" stroke={ringColor} strokeWidth="1" />
             <line x1="2" y1="50" x2="98" y2="50" stroke={ringColor} strokeWidth="1" />
             
             {/* Blip - Pulsing */}
             <circle cx="70" cy="30" r="4" fill="#ffcc00">
               <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite" />
               <animate attributeName="r" values="4;6;4" dur="2s" repeatCount="indefinite" />
             </circle>
             
             {/* Sweep - Sector Scan */}
             <path d="M 50 50 L 80 10 A 50 50 0 0 1 90 20 Z" fill="url(#radar-sweep)" opacity="0.4">
                <animateTransform 
                  attributeName="transform" 
                  type="rotate" 
                  from="0 50 50" 
                  to="360 50 50" 
                  dur="4s" 
                  repeatCount="indefinite" 
                />
             </path>
             
             <defs>
               <linearGradient id="radar-sweep" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#00f3ff" stopOpacity="0" />
                  <stop offset="100%" stopColor="#00f3ff" stopOpacity="0.8" />
               </linearGradient>
             </defs>
          </svg>
       </div>

       <div className="flex flex-col items-center text-center">
          <span className="text-[9px] text-warning font-mono tracking-widest uppercase mb-0.5">INCOMING</span>
          <div className="text-sm font-bold leading-tight truncate w-full" style={{ color: textColor }}>{event}</div>
          <div className="text-xs text-cyan-500 font-mono mt-0.5 bg-cyan-950/30 px-2 rounded-full border border-cyan-900">{time}</div>
       </div>
    </div>
  );
};

// --- Cyber Reticle (Animated) ---
export const CyberReticle: React.FC<{ label: string, value: number, isLight?: boolean }> = ({ label, value, isLight = false }) => {
  const textColor = isLight ? '#0f172a' : '#ffffff';
  
  return (
    <div className="w-full h-full flex flex-col items-center justify-center relative overflow-hidden">
       <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
         {/* Rotating Dashed Ring - Slow */}
         <svg viewBox="0 0 100 100" className="w-[140px] h-[140px] absolute opacity-20 animate-[spin_60s_linear_infinite]">
            <circle cx="50" cy="50" r="48" stroke="#00f3ff" strokeWidth="0.5" strokeDasharray="5 5" fill="none" />
         </svg>
         
         {/* Brackets - Breathing */}
         <div className="w-32 h-20 border-x-2 border-cyan-500/50 absolute transition-transform duration-[3000ms] animate-[pulse_3s_ease-in-out_infinite]"></div>
         <div className="w-28 h-24 border-y-2 border-cyan-500/50 absolute transition-transform duration-[3000ms] animate-[pulse_3s_ease-in-out_infinite]"></div>
       </div>
       
       <div className={`relative z-10 text-center ${isLight ? 'bg-white/60' : 'bg-[#0a0a12]/50'} backdrop-blur-sm px-4 py-2 border border-cyan-900/30 rounded-sm`}>
          <div className="text-3xl font-mono font-bold tracking-widest drop-shadow-[0_0_5px_rgba(0,243,255,0.5)]" style={{ color: textColor }}>{value}</div>
          <div className="text-[9px] text-gray-500 uppercase mt-1 tracking-[0.2em]">{label}</div>
       </div>
    </div>
  );
};

// --- Cyber Range Bar (Animated) ---
export const CyberRangeBar: React.FC<{ range: string, isLight?: boolean }> = ({ range, isLight = false }) => {
  const textColor = isLight ? '#0f172a' : '#ffffff';
  const trackColor = isLight ? '#cbd5e1' : '#1a1a2e';
  
  return (
    <div className="w-full h-full flex flex-col justify-center px-4 relative overflow-hidden">
      {/* Background Oscillation */}
      <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-transparent via-cyan-500/5 to-transparent animate-[shimmer_3s_infinite] -skew-x-12 pointer-events-none"></div>

      <div className="flex justify-between text-[9px] text-gray-500 font-mono mb-3 uppercase tracking-wider relative z-10">
        <span>Low Bound</span>
        <span>High Bound</span>
      </div>
      
      <div className="relative h-8 w-full flex items-center mb-2">
        {/* Track */}
        <div className="absolute inset-0 w-full h-[1px] top-1/2" style={{ backgroundColor: trackColor }}></div>
        
        {/* Animated Bars */}
        <div className="absolute right-1/2 h-1 bg-gradient-to-l from-cyan-500 to-transparent w-[40%] opacity-60 animate-[pulse_4s_infinite]"></div>
        <div className="absolute left-1/2 h-1 bg-gradient-to-r from-cyan-500 to-transparent w-[40%] opacity-60 animate-[pulse_4s_infinite]"></div>
        
        {/* Center Marker - Oscillating */}
        <div className="absolute left-1/2 -translate-x-1/2 w-0.5 h-4 bg-cyan-500 shadow-[0_0_10px_cyan] z-10">
             <div className="absolute -top-1 -left-1 w-2.5 h-2.5 bg-cyan-500/20 rounded-full animate-ping"></div>
        </div>
        
        {/* End Ticks */}
        <div className="absolute left-[10%] w-[1px] h-3 bg-gray-500 top-1/2 -translate-y-1/2"></div>
        <div className="absolute right-[10%] w-[1px] h-3 bg-gray-500 top-1/2 -translate-y-1/2"></div>
      </div>
      
      <div className="text-center relative z-10">
        <span className={`text-lg font-mono font-bold tracking-widest ${isLight ? 'bg-white/80' : 'bg-[#1a1a2e]/80'} px-3 py-1 rounded-sm border border-cyan-900/50 shadow-[0_0_15px_rgba(0,0,0,0.1)]`} style={{ color: textColor }}>{range}</span>
      </div>
    </div>
  )
};

// --- Heatmap Cell Mock ---
export const HeatmapStrip: React.FC<{ value: string }> = ({ value }) => (
  <div className="flex h-8 w-full gap-1 mt-3">
    {[1, 2, 3, 4, 5, 6].map((i) => (
      <div 
        key={i} 
        className={`flex-1 rounded-sm border border-black ${i < 4 ? 'bg-red-500/20 shadow-[0_0_5px_rgba(255,0,0,0.2)]' : 'bg-green-500/40 shadow-[0_0_5px_rgba(0,255,0,0.2)]'}`}
        style={{ opacity: i * 0.15 + 0.1 }}
      />
    ))}
  </div>
);