export interface PredictionRequest {
  question: string;
  response: string;
}

export interface PredictionResponse {
  label: EvasivenessLabel;
  scores: Record<EvasivenessLabel, number>;
  margin: number;
  reviewRecommended: boolean;
  truncated: boolean;
  tokenCount: number;
}

export type EvasivenessLabel =
  | 'Direct'
  | 'Partially Evasive'
  | 'Fully Evasive';
