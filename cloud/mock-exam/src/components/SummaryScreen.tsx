import { motion } from "framer-motion";
import { useEffect, useState } from "react";

interface SummaryScreenProps {
  score: number;
  total: number;
  onRestart: () => void;
}

export function SummaryScreen({ score, total, onRestart }: SummaryScreenProps) {
  const percentage = Math.round((score / total) * 100);
  const [typedTitle, setTypedTitle] = useState("");

  const title = "SYSTEM DIAGNOSTICS: EXAM COMPLETE";

  useEffect(() => {
    let currentText = "";
    let i = 0;
    const interval = setInterval(() => {
      if (i < title.length) {
        currentText += title.charAt(i);
        setTypedTitle(currentText);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 50);
    return () => clearInterval(interval);
  }, []);

  // ASCII Progress bar generator e.g. [||||||||||.....]
  const renderProgressBar = (percent: number) => {
    const totalBlocks = 20;
    const filledBlocks = Math.round((percent / 100) * totalBlocks);
    const emptyBlocks = totalBlocks - filledBlocks;
    
    return `[${'|'.repeat(filledBlocks)}${'.'.repeat(emptyBlocks)}]`;
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-2xl mx-auto mt-8 px-4"
    >
      <div className="terminal-border">
        {/* Terminal Header */}
        <div className="terminal-header -mt-7 mx-auto w-fit px-4 bg-background border border-primary">
          +--- DIAGNOSTIC RESULTS ---+
        </div>

        <div className="p-4 sm:p-8 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-xl sm:text-2xl font-bold uppercase text-primary">
              {typedTitle}
              <span className="animate-pulse inline-block w-3 h-6 bg-primary ml-1 align-bottom"></span>
            </h2>
            <div className="text-primary/50 text-sm">================================================</div>
          </div>

          <div className="flex flex-col items-center justify-center space-y-4 py-4">
            <div className="text-sm uppercase text-secondary">FINAL SCORE</div>
            <div className="text-5xl sm:text-6xl font-black text-primary tracking-widest">
              {score} <span className="text-2xl sm:text-3xl text-primary/50">/ {total}</span>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex flex-col items-center gap-2">
              <div className="flex justify-between w-full max-w-xs text-sm font-bold uppercase">
                <span>ACCURACY</span>
                <span>{percentage}%</span>
              </div>
              <div className="text-xl tracking-[0.2em] font-bold text-primary">
                {renderProgressBar(percentage)}
              </div>
            </div>
          </div>

          <div className="pt-6 text-center text-sm sm:text-base border-t border-dashed border-primary/50">
            <p className={percentage >= 70 ? "text-primary" : "text-secondary"}>
              {percentage >= 70
                ? "> STATUS: PASSED. EXCELLENT UNDERSTANDING DETECTED."
                : "> STATUS: FAILED. FURTHER TRAINING REQUIRED."}
            </p>
          </div>
        </div>
        
        <div className="mt-4 pt-4 border-t border-dashed border-primary/50 flex justify-center">
          <button 
            onClick={onRestart} 
            className="terminal-btn px-8 py-3 text-sm sm:text-base w-full sm:w-auto"
          >
            &gt; [ REBOOT SYSTEM ]
          </button>
        </div>
      </div>
    </motion.div>
  );
}
