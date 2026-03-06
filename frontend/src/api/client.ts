import axios from "axios";
import type { IdeaIntake, StartupContext, SessionStatus } from "./types";

const api = axios.create({ baseURL: "/api" });

export async function createSession(intake: IdeaIntake): Promise<string> {
  const { data } = await api.post("/session/create", intake);
  return data.session_id;
}

export async function runStage(sessionId: string, stage: string) {
  const { data } = await api.post("/stage/run", {
    session_id: sessionId,
    stage,
  });
  return data;
}

export async function getSessionOutput(
  sessionId: string
): Promise<StartupContext> {
  const { data } = await api.get(`/session/${sessionId}/output`);
  return data;
}

export async function getSessionStatus(
  sessionId: string
): Promise<SessionStatus> {
  const { data } = await api.get(`/session/${sessionId}/status`);
  return data;
}

export async function rerunAgent(
  sessionId: string,
  agentName: string,
  overrides: Record<string, any>
): Promise<StartupContext> {
  const { data } = await api.post("/agent/rerun", {
    session_id: sessionId,
    agent_name: agentName,
    overrides,
  });
  return data;
}

export async function getDownloadUrl(
  sessionId: string,
  fileType: string
): Promise<string> {
  const { data } = await api.get("/output/download", {
    params: { session_id: sessionId, file_type: fileType },
  });
  return data.download_url;
}

export function createSSEConnection(sessionId: string): EventSource {
  return new EventSource(`/api/stage/stream/${sessionId}`);
}
