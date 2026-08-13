import { useState, useMemo, useEffect } from "react";
import type { Question } from "@/types";
import { QuestionCard } from "./QuestionCard";
import { SummaryScreen } from "./SummaryScreen";
import { shuffle } from "@/utils/shuffle";

interface ExamManagerProps {
  questions: Question[];
  randomize?: boolean;
}

export function ExamManager({ questions, randomize = true }: ExamManagerProps) {
  const [examQuestions, setExamQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<boolean[]>([]);
  const [isFinished, setIsFinished] = useState(false);
  const [hasStarted, setHasStarted] = useState(false);
  
  const [typedHeader, setTypedHeader] = useState("");
  const headerText = "AWS ACADEMY CLOUD FOUNDATIONS";

  useMemo(() => {
    if (!hasStarted) {
      const qs = randomize ? shuffle(questions) : [...questions];
      setExamQuestions(qs);
      setAnswers(new Array(questions.length).fill(false));
      setHasStarted(true);
    }
  }, [questions, randomize, hasStarted]);

  useEffect(() => {
    let currentText = "";
    let i = 0;
    const interval = setInterval(() => {
      if (i < headerText.length) {
        currentText += headerText.charAt(i);
        setTypedHeader(currentText);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 50);
    return () => clearInterval(interval);
  }, []);

  const handleNext = (isCorrect: boolean) => {
    setAnswers((prev) => {
      const newAnswers = [...prev];
      newAnswers[currentIndex] = isCorrect;
      return newAnswers;
    });

    if (currentIndex < examQuestions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      setIsFinished(true);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setIsFinished(false);
    setHasStarted(false);
  };

  if (!hasStarted || examQuestions.length === 0) {
    return (
      <div className="min-h-screen bg-background text-primary flex items-center justify-center font-bold text-2xl tracking-widest">
        INITIALIZING SYSTEM<span className="animate-pulse">_</span>
      </div>
    );
  }

  return (
    <>
      <div className="scanlines"></div>
      <div className="min-h-screen bg-background text-foreground flex flex-col pt-8 pb-12 relative z-10 selection:bg-primary selection:text-black">
        <header className="w-full max-w-4xl mx-auto px-4 sm:px-6 mb-12">
          <h1 className="text-2xl sm:text-3xl font-black text-primary border-b-2 border-primary pb-2 inline-block">
            MOCK_EXAM_SYSTEM: {typedHeader}<span className="animate-pulse">_</span>
          </h1>
          <div className="mt-2 text-primary/70 text-sm">v1.0.0 (build 20260813) - ALL SYSTEMS NOMINAL</div>
        </header>

        <main className="flex-grow flex flex-col">
          {isFinished ? (
            <SummaryScreen
              score={answers.filter(Boolean).length}
              total={examQuestions.length}
              onRestart={handleRestart}
            />
          ) : (
            <QuestionCard
              question={examQuestions[currentIndex]}
              currentIndex={currentIndex}
              total={examQuestions.length}
              onNext={handleNext}
              onPrevious={handlePrevious} 
            />
          )}
        </main>
      </div>
    </>
  );
}
