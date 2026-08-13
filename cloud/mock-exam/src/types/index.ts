export interface Option {
  text: string;
  correct: boolean;
}

export interface Question {
  id: number;
  module: string;
  isNew: boolean;
  type: "single" | "multiple" | "boolean";
  question: string;
  options: Option[];
}
