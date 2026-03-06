import { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  getSessionOutput,
  getSessionStatus,
  rerunAgent,
  runStage,
} from "../api/client";
import type { StartupContext } from "../api/types";
import StageProgress from "../components/layout/StageProgress";
import AgentCard from "../components/agents/AgentCard";
import SynthesisCard from "../components/agents/SynthesisCard";
import OverrideModal from "../components/shared/OverrideModal";

const AGENT_META: Record<string, { icon: string; title: string; scoreField: string; scoreLabel: string }> = {
  shark_tank_agent: { icon: "🦈", title: "Shark Tank Agent", scoreField: "score", scoreLabel: "Investability" },
  vc_agent: { icon: "💼", title: "VC Agent", scoreField: "fundability_score", scoreLabel: "Fundability" },
  consultant_agent: { icon: "📊", title: "Consultant Agent", scoreField: "strategy_score", scoreLabel: "Strategy" },
  worst_case_customer_agent: { icon: "😤", title: "Worst-Case Customer", scoreField: "friction_score", scoreLabel: "Friction" },
};

export default function IdeationDashboard() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [ctx, setCtx] = useState<StartupContext | null>(null);
  const [showOverride, setShowOverride] = useState(false);
  const [rerunningAgent, setRerunningAgent] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    if (!id) return;
    const data = await getSessionOutput(id);
    setCtx(data);
  }, [id]);

  // Poll for updates
  useEffect(() => {
    fetchData();
    const interval = setInterval(async () => {
      if (!id) return;
      const status = await getSessionStatus(id);
      if (status.status === "completed" || Object.values(status.agent_statuses).every(s => s === "completed")) {
        clearInterval(interval);
      }
      fetchData();
    }, 3000);
    return () => clearInterval(interval);
  }, [id, fetchData]);

  const handleRerun = async (agentName: string) => {
    if (!id || !ctx) return;
    setRerunningAgent(agentName);
    try {
      const updated = await rerunAgent(id, agentName, {});
      setCtx(updated);
    } finally {
      setRerunningAgent(null);
    }
  };

  const handleOverrideSave = async (overrides: Record<string, any>) => {
    if (!id || !ctx) return;
    // Re-run all agents with new assumptions
    const updated = await rerunAgent(id, "shark_tank_agent", overrides);
    setCtx(updated);
  };

  const handleProceed = async () => {
    if (!id) return;
    await runStage(id, "execution");
    navigate(`/session/${id}/execution`);
  };

  if (!ctx) {
    return (
      <div className="min-h-screen bg-[#f8f9fa]">
        <StageProgress current="ideation" />
        <div className="max-w-6xl mx-auto py-16 text-center">
          <div className="text-4xl mb-4 pulse-loading">🧠</div>
          <p className="text-gray-500">Loading session...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f8f9fa]">
      <StageProgress current="ideation" sessionId={id} />

      <div className="max-w-6xl mx-auto py-8 px-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold">Ideation Analysis</h1>
          <p className="text-gray-500 text-sm mt-1">
            {ctx.idea_intake.raw_idea.slice(0, 100)}...
          </p>
        </div>

        {/* 2x2 Agent Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.entries(AGENT_META).map(([name, meta]) => {
            const output = ctx.ideation_outputs[name] || { status: "pending" };
            const status = rerunningAgent === name ? "running" : output.status || "pending";

            return (
              <AgentCard
                key={name}
                icon={meta.icon}
                title={meta.title}
                status={status}
                grounding_score={output.grounding_score || 0}
                scoreLabel={meta.scoreLabel}
                scoreValue={output[meta.scoreField] || 0}
                sourceDocs={output.source_documents || []}
                onRerun={() => handleRerun(name)}
                onUpdateAssumptions={() => setShowOverride(true)}
              >
                <AgentBody name={name} output={output} />
              </AgentCard>
            );
          })}
        </div>

        {/* Synthesis */}
        <SynthesisCard
          data={ctx.ideation_outputs.synthesis || null}
          onProceed={handleProceed}
        />
      </div>

      {showOverride && ctx && (
        <OverrideModal
          intake={ctx.idea_intake}
          onSave={handleOverrideSave}
          onClose={() => setShowOverride(false)}
        />
      )}
    </div>
  );
}

function AgentBody({ name, output }: { name: string; output: any }) {
  if (output.status !== "completed") return null;

  if (name === "shark_tank_agent") {
    return (
      <div className="space-y-3 text-sm">
        <div className="flex gap-4">
          <span className="text-green-600">Funded: {output.funded_count}</span>
          <span className="text-red-500">Rejected: {output.rejected_count}</span>
        </div>
        {output.common_rejection_reasons?.length > 0 && (
          <div>
            <p className="font-medium text-xs text-gray-500 mb-1">WHY REJECTED</p>
            <ul className="space-y-0.5">
              {output.common_rejection_reasons.map((r: string, i: number) => (
                <li key={i} className="text-gray-700">• {r}</li>
              ))}
            </ul>
          </div>
        )}
        {output.your_gaps?.length > 0 && (
          <div>
            <p className="font-medium text-xs text-gray-500 mb-1">YOUR GAPS</p>
            <ul className="space-y-0.5">
              {output.your_gaps.map((g: string, i: number) => (
                <li key={i} className="text-yellow-600">⚠ {g}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  if (name === "vc_agent") {
    return (
      <div className="space-y-3 text-sm">
        <p className="text-gray-600">{output.comparable_companies_analyzed} companies analyzed</p>
        {output.positive_signals?.length > 0 && (
          <div>
            <p className="font-medium text-xs text-gray-500 mb-1">POSITIVE SIGNALS</p>
            {output.positive_signals.map((s: string, i: number) => (
              <p key={i} className="text-green-700">+ {s}</p>
            ))}
          </div>
        )}
        {output.red_flags?.length > 0 && (
          <div>
            <p className="font-medium text-xs text-gray-500 mb-1">RED FLAGS</p>
            {output.red_flags.map((f: string, i: number) => (
              <p key={i} className="text-red-500">✕ {f}</p>
            ))}
          </div>
        )}
        {output.recommended_funding_path && (
          <p className="text-[#1a73e8] font-medium">Path: {output.recommended_funding_path}</p>
        )}
      </div>
    );
  }

  if (name === "consultant_agent") {
    return (
      <div className="space-y-3 text-sm">
        {output.market_size_verified && (
          <div>
            <p className="font-medium text-xs text-gray-500 mb-1">MARKET SIZE</p>
            <p className="text-lg font-semibold">{output.market_size_verified}</p>
            <p className="text-xs text-gray-400">{output.market_size_source}</p>
          </div>
        )}
        {output.top_competitors?.length > 0 && (
          <div>
            <p className="font-medium text-xs text-gray-500 mb-1">COMPETITORS</p>
            {output.top_competitors.map((c: any, i: number) => (
              <p key={i} className="text-gray-700">
                <span className="font-medium">{c.name}</span> — {c.weakness}
              </p>
            ))}
          </div>
        )}
        {output.strategic_gap && (
          <p className="text-gray-600 italic">{output.strategic_gap}</p>
        )}
      </div>
    );
  }

  if (name === "worst_case_customer_agent") {
    return (
      <div className="space-y-3 text-sm">
        {Object.entries(output.objections_by_persona || {}).map(
          ([persona, objections]: [string, any]) => (
            <div key={persona}>
              <p className="font-medium text-xs text-gray-500 mb-1">
                {persona.replace(/_/g, " ").toUpperCase()}
              </p>
              {objections.map((o: string, i: number) => (
                <p key={i} className="text-red-600 text-sm">✕ "{o}"</p>
              ))}
            </div>
          )
        )}
      </div>
    );
  }

  return <p className="text-sm text-gray-500">{output.summary}</p>;
}
