import { ExamManager } from "./components/ExamManager";
import { PasswordGate } from "./components/PasswordGate";
import questionsData from "./data/questions.json";
import type { Question } from "./types";

function App() {
  const questions = questionsData as Question[];

  return (
    <PasswordGate>
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-50">
        <header className="bg-white dark:bg-slate-900 shadow-sm border-b sticky top-0 z-10">
          <div className="max-w-4xl mx-auto px-4 h-16 flex items-center justify-center">
            <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
              Mock Exam: AWS Academy Cloud Foundations
            </h1>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <ExamManager questions={questions} randomize={true} />
        </main>
      </div>
    </PasswordGate>
  );
}

export default App;
