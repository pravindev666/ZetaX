import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, HelpCircle, AlertTriangle } from 'lucide-react';

// --- Tech Corner Component ---
const CornerBrackets = ({ active = false, color = 'cyan' }) => {
  const colorClass = color === 'green' ? 'border-bullish' : color === 'red' ? 'border-bearish' : 'border-neutral';

  return (
    <>
      <div className={`absolute top-0 left-0 w-3 h-3 border-l-2 border-t-2 ${colorClass} transition-all duration-300 ${active ? 'opacity-100 w-4 h-4' : 'opacity-0'}`} />
      <div className={`absolute top-0 right-0 w-3 h-3 border-r-2 border-t-2 ${colorClass} transition-all duration-300 ${active ? 'opacity-100 w-4 h-4' : 'opacity-0'}`} />
      <div className={`absolute bottom-0 left-0 w-3 h-3 border-l-2 border-b-2 ${colorClass} transition-all duration-300 ${active ? 'opacity-100 w-4 h-4' : 'opacity-0'}`} />
      <div className={`absolute bottom-0 right-0 w-3 h-3 border-r-2 border-b-2 ${colorClass} transition-all duration-300 ${active ? 'opacity-100 w-4 h-4' : 'opacity-0'}`} />
    </>
  );
};

// --- Tile Component ---
interface GlassTileProps {
  title: string;
  verdict: string;
  onHelp: () => void;
  children: React.ReactNode;
  accent?: 'bullish' | 'bearish' | 'neutral' | 'warning';
  className?: string;
}

export const GlassTile: React.FC<GlassTileProps> = ({
  title,
  verdict,
  onHelp,
  children,
  accent = 'neutral',
  className = ''
}) => {
  const [hovered, setHovered] = React.useState(false);

  const getThemeColors = () => {
    switch (accent) {
      case 'bullish': return { border: 'group-hover:border-bullish', text: 'text-bullish', glow: 'group-hover:shadow-neon-green', bracket: 'green' };
      case 'bearish': return { border: 'group-hover:border-bearish', text: 'text-bearish', glow: 'group-hover:shadow-neon-red', bracket: 'red' };
      case 'warning': return { border: 'group-hover:border-warning', text: 'text-warning', glow: 'group-hover:shadow-[0_0_15px_rgba(255,204,0,0.4)]', bracket: 'cyan' };
      default: return { border: 'group-hover:border-neutral', text: 'text-neutral', glow: 'group-hover:shadow-neon-blue', bracket: 'cyan' };
    }
  };

  const theme = getThemeColors();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className={`
        relative flex flex-col justify-between 
        bg-surface/90 backdrop-blur-sm 
        border border-border
        rounded-sm overflow-hidden 
        group transition-all duration-300 
        hover:scale-[1.02] hover:z-10
        ${theme.border} ${theme.glow}
        min-h-[200px] cursor-default
        ${className}
      `}
    >
      <CornerBrackets active={hovered} color={theme.bracket} />

      {/* Header */}
      <div className="flex justify-between items-center p-3 relative z-10 border-b border-border/50">
        <h3 className="text-sm font-bold text-text-muted font-header tracking-widest uppercase flex items-center gap-2">
          {accent === 'bullish' && <span className="w-1.5 h-1.5 bg-bullish rounded-full animate-pulse" />}
          {accent === 'bearish' && <span className="w-1.5 h-1.5 bg-bearish rounded-full animate-pulse" />}
          {title}
        </h3>
        <button
          onClick={(e) => { e.stopPropagation(); onHelp(); }}
          className="text-border hover:text-cyan-500 transition-colors"
        >
          <HelpCircle size={18} />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 p-4 flex flex-col justify-center relative z-10 text-text-main">
        {children}
      </div>

      {/* Footer Verdict - increased height with text wrapping */}
      <div className={`
        w-full py-3 px-3 border-t border-border
        bg-background group-hover:bg-surface transition-colors
        min-h-[52px]
      `}>
        <span className="text-[9px] text-text-muted font-mono uppercase tracking-widest block mb-1">VERDICT</span>
        <p className={`text-xs font-mono font-bold ${theme.text} tracking-tight leading-tight line-clamp-2`}>
          {verdict.toUpperCase()}
        </p>
      </div>
    </motion.div>
  );
};

// --- Modal ---
interface ModalProps {
  isOpen: boolean;
  onClose?: () => void;
  title: string;
  children: React.ReactNode;
  preventClose?: boolean;
}

const shutterVariants = {
  hidden: {
    scaleY: 0,
    opacity: 0,
    filter: "blur(10px)",
  },
  visible: {
    scaleY: 1,
    opacity: 1,
    filter: "blur(0px)",
    transition: {
      duration: 0.4,
      ease: [0.22, 1, 0.36, 1]
    }
  },
  exit: {
    scaleY: 0,
    opacity: 0,
    filter: "blur(10px)",
    transition: {
      duration: 0.3,
      ease: [0.22, 1, 0.36, 1]
    }
  }
};

export const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children, preventClose }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          key="modal-backdrop"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6"
        >
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/80 backdrop-blur-md"
            onClick={!preventClose ? onClose : undefined}
          ></div>

          {/* Modal Container */}
          <motion.div
            variants={shutterVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            style={{ transformOrigin: 'center' }}
            className="relative w-full max-w-lg bg-surface border-y-2 border-cyan-500/50 shadow-[0_0_50px_rgba(0,243,255,0.15)] overflow-hidden flex flex-col max-h-[90vh]"
          >
            {/* Terminal Top Bar */}
            <div className="h-6 bg-cyan-950/30 border-b border-cyan-900/50 flex items-center px-2 gap-1.5">
              <div className="w-2 h-2 rounded-full bg-red-500/50"></div>
              <div className="w-2 h-2 rounded-full bg-yellow-500/50"></div>
              <div className="w-2 h-2 rounded-full bg-green-500/50"></div>
              <div className="ml-auto text-[8px] font-mono text-cyan-700">TERMINAL_ID: RBX_099</div>
            </div>

            <CornerBrackets active={true} color="cyan" />

            {/* Header */}
            <div className="flex justify-between items-center p-6 border-b border-border bg-surface shrink-0">
              <h2 className="text-2xl font-header font-bold text-text-main uppercase tracking-widest flex items-center gap-2">
                <span className="text-cyan-500 text-lg">System</span> <span className="text-gray-500">//</span> {title}
              </h2>
              {!preventClose && onClose && (
                <button onClick={onClose} className="text-text-muted hover:text-text-main hover:rotate-90 transition-transform duration-300">
                  <X size={24} />
                </button>
              )}
            </div>

            {/* Scrollable Content */}
            <div className="p-6 overflow-y-auto text-text-main text-base font-light leading-relaxed scrollbar-thin scrollbar-thumb-cyan-900 scrollbar-track-transparent">
              {children}
            </div>

            {/* Terminal Bottom Decoration */}
            <div className="h-1 bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent w-full"></div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

// --- Segmented Control ---
interface SegmentedControlProps {
  options: string[];
  selected: string;
  onChange: (opt: string) => void;
}

export const SegmentedControl: React.FC<SegmentedControlProps> = ({ options, selected, onChange }) => (
  <div className="flex bg-background rounded-sm p-1 border border-border">
    {options.map(opt => (
      <button
        key={opt}
        onClick={() => onChange(opt)}
        className={`px-4 py-2 text-sm font-mono font-bold transition-all duration-300 rounded-sm ${selected === opt
            ? 'bg-cyan-500/10 text-cyan-500 border border-cyan-500/50 shadow-[0_0_10px_rgba(0,243,255,0.2)]'
            : 'text-text-muted hover:text-text-main hover:bg-surface'
          }`}
      >
        {opt}
      </button>
    ))}
  </div>
);

// --- Status Dot ---
export const StatusDot: React.FC<{ status: 'ok' | 'warn' | 'err' }> = ({ status }) => {
  const color = status === 'ok' ? 'bg-bullish' : status === 'warn' ? 'bg-warning' : 'bg-bearish';
  return (
    <div className="flex items-center space-x-2 bg-surface px-3 py-1 rounded-full border border-border">
      <span className={`w-2 h-2 rounded-full ${color} shadow-[0_0_8px_currentColor] animate-pulse`}></span>
      <span className="text-[10px] text-text-muted font-mono uppercase tracking-wider">Sys {status}</span>
    </div>
  );
};