export type UserRole = 'admin' | 'user';

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export type ResearchJobStatus =
  | 'pending'
  | 'planning'
  | 'researching'
  | 'synthesizing'
  | 'critiquing'
  | 'completed'
  | 'failed';

export interface ResearchJob {
  id: string;
  query: string;
  title: string | null;
  status: ResearchJobStatus;
  created_at: string;
  updated_at: string;
}

export interface Source {
  id: string;
  title: string;
  url: string;
  snippet: string | null;
  source_type: string;
  relevance: number;
}

export interface ResearchJobDetail extends ResearchJob {
  sub_questions: string[] | null;
  report: string | null;
  executive_summary: string | null;
  faithfulness_score: number | null;
  relevance_score: number | null;
  tokens_in: number;
  tokens_out: number;
  cost_usd: number;
  error_message: string | null;
  sources: Source[];
}

export interface ResearchJobList {
  items: ResearchJob[];
  total: number;
}
