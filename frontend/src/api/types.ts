export interface IdeaIntake {
  raw_idea: string;
  industry: string;
  stage: string;
  team_size: number;
  geography: string;
  budget_range: string;
  target_customer: string;
  b2b_or_b2c: string;
  has_cofounder: boolean;
}

export interface AgentOutput {
  status: "pending" | "running" | "completed" | "error" | "stale";
  grounding_score: number;
  source_documents: string[];
  raw_output: string;
  data?: Record<string, any>;
  [key: string]: any;
}

export interface SynthesisOutput {
  overall_viability_score: number;
  top_strengths: string[];
  top_risks: string[];
  proceed_to_execution: boolean;
  recommendation?: string;
}

export interface StartupContext {
  session_id: string;
  version: number;
  created_at: string;
  last_updated: string;
  idea_intake: IdeaIntake;
  ideation_outputs: Record<string, any>;
  execution_outputs: Record<string, any>;
  operation_outputs: Record<string, any>;
  user_overrides: { override_history: any[] };
}

export interface SessionStatus {
  session_id: string;
  stage: string;
  agent_statuses: Record<string, string>;
  status: string;
}
