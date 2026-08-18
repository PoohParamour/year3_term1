import { motion } from "framer-motion";
import { useEffect, useState } from "react";

import type { Question } from "@/types";

interface SummaryScreenProps {
  score: number;
  total: number;
  onRestart: () => void;
  examQuestions: Question[];
  answers: boolean[];
}

export function SummaryScreen({ score, total, onRestart, examQuestions, answers }: SummaryScreenProps) {
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

          {/* Weak Topics Section */}
          <div className="pt-6 border-t border-dashed border-primary/50">
            <h3 className="text-lg font-bold text-primary mb-4 flex items-center gap-2">
              <span className="text-secondary select-none">sys@mock:~$</span>
              <span>./analyze_weaknesses.sh</span>
            </h3>
            
            <div className="space-y-3">
              {(() => {
                const moduleStats: Record<string, { total: number; correct: number }> = {};
                examQuestions.forEach((q, idx) => {
                  if (!moduleStats[q.module]) {
                    moduleStats[q.module] = { total: 0, correct: 0 };
                  }
                  moduleStats[q.module].total += 1;
                  if (answers[idx]) {
                    moduleStats[q.module].correct += 1;
                  }
                });

                const weakModules = Object.entries(moduleStats)
                  .map(([module, stats]) => ({
                    module,
                    accuracy: Math.round((stats.correct / stats.total) * 100),
                  }))
                  .filter((m) => m.accuracy < 70)
                  .sort((a, b) => a.accuracy - b.accuracy);

                if (weakModules.length === 0) {
                  return (
                    <div className="text-primary/70">
                      &gt; NO CRITICAL WEAKNESSES DETECTED. ALL MODULES &gt;= 70%.
                    </div>
                  );
                }

                return (
                  <>
                    <div className="text-secondary/80 text-sm mb-2">
                      [!] DETECTED MODULES WITH ACCURACY &lt; 70%:
                    </div>
                    {weakModules.map((m, idx) => (
                      <div key={idx} className="flex justify-between items-center bg-primary/5 p-2 border-l-2 border-destructive">
                        <span className="font-medium text-destructive">{m.module}</span>
                        <span className="text-destructive font-bold">{m.accuracy}%</span>
                      </div>
                    ))}
                    <div className="text-sm text-primary/70 mt-4">
                      &gt; RECOMMENDATION: REVIEW THESE MODULES BEFORE RETAKING EXAM.
                    </div>
                  </>
                );
              })()}
            </div>
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
