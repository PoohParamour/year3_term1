import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { Question, Option } from "@/types";
import { shuffle } from "@/utils/shuffle";

interface QuestionCardProps {
  question: Question;
  currentIndex: number;
  total: number;
  onNext: (isCorrect: boolean) => void;
  onPrevious?: () => void;
}

export function QuestionCard({ question, currentIndex, total, onNext, onPrevious }: QuestionCardProps) {
  const [selectedAnswers, setSelectedAnswers] = useState<string[]>([]);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const shuffledOptions = useMemo(() => shuffle(question.options), [question.id]);
  const isMultiple = question.type === "multiple";

  useMemo(() => {
    setSelectedAnswers([]);
    setIsSubmitted(false);
  }, [question.id]);

  const handleToggleMultiple = (text: string) => {
    if (isSubmitted) return;
    setSelectedAnswers((prev) =>
      prev.includes(text) ? prev.filter((t) => t !== text) : [...prev, text]
    );
  };

  const handleSingleSelect = (text: string) => {
    if (isSubmitted) return;
    setSelectedAnswers([text]);
  };

  const checkIsCorrect = () => {
    const correctOptions = shuffledOptions.filter((o) => o.correct).map((o) => o.text);
    if (isMultiple) {
      if (selectedAnswers.length !== correctOptions.length) return false;
      return correctOptions.every((c) => selectedAnswers.includes(c));
    } else {
      return correctOptions[0] === selectedAnswers[0];
    }
  };

  const handleSubmit = () => {
    if (selectedAnswers.length === 0) return;
    setIsSubmitted(true);
  };

  const handleNext = () => {
    onNext(checkIsCorrect());
  };

  const isOptionCorrect = (opt: Option) => opt.correct;
  const isOptionSelected = (opt: Option) => selectedAnswers.includes(opt.text);

  const getOptionStyle = (opt: Option) => {
    if (!isSubmitted) {
      return isOptionSelected(opt)
        ? "bg-primary text-black"
        : "text-primary hover:bg-primary/20";
    }

    if (isOptionSelected(opt) && isOptionCorrect(opt)) {
      return "bg-primary text-black border-l-4 border-l-black"; // OK
    }
    if (isOptionSelected(opt) && !isOptionCorrect(opt)) {
      return "bg-destructive text-black border-l-4 border-l-black"; // ERR
    }
    if (!isOptionSelected(opt) && isOptionCorrect(opt)) {
      return "border border-dashed border-primary text-primary opacity-80"; // MISSED
    }
    return "text-muted-foreground opacity-50";
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4 sm:px-6">
      <div className="mb-4 space-y-1">
        <div className="flex justify-between text-xs sm:text-sm font-bold uppercase tracking-widest text-primary/70">
          <span>PROGRESS [{currentIndex + 1}/{total}]</span>
          <span>{Math.round(((currentIndex + 1) / total) * 100)}%</span>
        </div>
        <div className="w-full bg-muted border border-border h-3 relative">
          <motion.div
            className="absolute top-0 left-0 h-full bg-primary"
            initial={{ width: 0 }}
            animate={{ width: `${((currentIndex + 1) / total) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={question.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          <div className="terminal-border group">
            {/* Terminal Header */}
            <div className="terminal-header -mt-7 mx-auto w-fit px-4 bg-background border border-primary">
              +--- MODULE: {question.module.toUpperCase()} ---+
            </div>

            <div className="p-2 sm:p-4 space-y-6">
              {/* Question Area */}
              <div className="space-y-4">
                <div className="flex items-start gap-2">
                  <span className="text-secondary select-none">sys@mock:~$</span>
                  <span className="opacity-70">cat question_{currentIndex + 1}.txt</span>
                </div>
                {isMultiple && (
                  <div className="text-secondary text-xs uppercase animate-pulse">
                    [!] SELECT MULTIPLE OPTIONS
                  </div>
                )}
                <div className="text-lg sm:text-xl font-medium leading-relaxed min-h-[60px]">
                  {question.question}
                  <span className="animate-pulse inline-block w-2.5 h-5 bg-primary ml-1 align-bottom"></span>
                </div>
              </div>

              {/* Separator */}
              <div className="text-primary/30 select-none overflow-hidden whitespace-nowrap">
                ====================================================================================================
              </div>

              {/* Options Area */}
              <div className="space-y-2 mt-4">
                <div className="flex items-start gap-2 mb-2">
                  <span className="text-secondary select-none">sys@mock:~$</span>
                  <span className="opacity-70">./select_answer.sh</span>
                </div>

                {shuffledOptions.map((opt, idx) => {
                  const selected = isOptionSelected(opt);
                  const isCorrect = isOptionCorrect(opt);
                  const showFeedback = isSubmitted;

                  return (
                    <motion.div
                      key={idx}
                      whileHover={!isSubmitted ? { x: 5 } : {}}
                      animate={
                        showFeedback && selected
                          ? isCorrect
                            ? { x: [0, 5, 0] }
                            : { x: [0, -5, 5, -5, 5, 0] }
                          : {}
                      }
                      onClick={() => {
                        if (isMultiple) handleToggleMultiple(opt.text);
                        else handleSingleSelect(opt.text);
                      }}
                      className={`
                        flex items-start gap-3 p-2 cursor-pointer transition-colors
                        ${getOptionStyle(opt)}
                      `}
                    >
                      <div className="flex-shrink-0 font-bold select-none whitespace-pre mt-0.5">
                        {isMultiple ? (selected ? "[X]" : "[ ]") : (selected ? "(*)" : "( )")}
                      </div>
                      <div className="flex-grow text-sm sm:text-base leading-relaxed">
                        {opt.text}
                      </div>
                      
                      {showFeedback && (
                        <div className="flex-shrink-0 font-bold ml-2">
                          {isCorrect && selected && <span className="text-black bg-primary px-1">[OK]</span>}
                          {!isCorrect && selected && <span className="text-black bg-destructive px-1">[ERR]</span>}
                          {isCorrect && !selected && <span className="text-primary bg-primary/20 px-1">[MISSED]</span>}
                        </div>
                      )}
                    </motion.div>
                  );
                })}
              </div>

              {isSubmitted && (
                <motion.div 
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="mt-6 p-4 border border-dashed border-primary/50 bg-primary/5 rounded-sm"
                >
                  <div className="flex items-start gap-2 mb-2">
                    <span className="text-secondary select-none">sys@mock:~$</span>
                    <span className="opacity-70">cat explanation.txt</span>
                  </div>
                  <div className="text-sm sm:text-base leading-relaxed text-primary/90">
                    {question.explanation || "ไม่มีคำอธิบายในระบบสำหรับข้อนี้ (No explanation provided for this question)"}
                  </div>
                </motion.div>
              )}
            </div>

            {/* Footer / Actions */}
            <div className="mt-8 pt-4 border-t border-dashed border-primary/50 flex flex-col sm:flex-row justify-between items-center gap-4">
              <button
                onClick={onPrevious}
                disabled={currentIndex === 0}
                className="terminal-btn px-4 py-2 text-sm w-full sm:w-auto disabled:opacity-30 disabled:hover:bg-transparent disabled:hover:text-primary disabled:cursor-not-allowed"
              >
                [ &lt; PREVIOUS ]
              </button>

              {!isSubmitted ? (
                <button
                  onClick={handleSubmit}
                  disabled={selectedAnswers.length === 0}
                  className="terminal-btn px-8 py-2 text-sm w-full sm:w-auto disabled:opacity-30 disabled:hover:bg-transparent disabled:hover:text-primary disabled:cursor-not-allowed border-2"
                >
                  [ EXECUTE ]
                </button>
              ) : (
                <button
                  onClick={handleNext}
                  className="px-8 py-2 text-sm w-full sm:w-auto bg-primary text-black font-bold uppercase hover:bg-white hover:text-black focus-visible:ring-2 focus-visible:ring-offset-2 border-2 border-primary"
                >
                  {currentIndex === total - 1 ? "[ SHOW RESULTS ]" : "[ NEXT >> ]"}
                </button>
              )}
            </div>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
