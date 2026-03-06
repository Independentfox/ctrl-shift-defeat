import { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import { getSessionOutput } from "../api/client";
import type { StartupContext } from "../api/types";
import StageProgress from "../components/layout/StageProgress";
import GroundingBar from "../components/agents/GroundingBar";
import { MapPin, Calendar, CheckSquare } from "lucide-react";

export default function OperationDashboard() {
  const { id } = useParams<{ id: string }>();
  const [ctx, setCtx] = useState<StartupContext | null>(null);

  const fetchData = useCallback(async () => {
    if (!id) return;
    const data = await getSessionOutput(id);
    setCtx(data);
  }, [id]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 4000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const ops = ctx?.operation_outputs;

  return (
    <div className="min-h-screen bg-[#f8f9fa]">
      <StageProgress current="operation" />
      <div className="max-w-3xl mx-auto py-8 px-6">
        <h1 className="text-2xl font-bold mb-2">Operations Roadmap</h1>
        <p className="text-gray-500 text-sm mb-6">
          Constraint-driven plan based on your financial reality
        </p>

        {ops?.status === "completed" ? (
          <>
            {/* Financial Reality Box */}
            {ops.financial_reality && (
              <div className="card p-5 mb-6">
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-[#1a73e8]" />
                  Your Financial Reality
                </h3>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <p className="text-xs text-gray-500">Burn Rate</p>
                    <p className="font-semibold">{ops.financial_reality.burn_rate}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Runway</p>
                    <p className="font-semibold">{ops.financial_reality.runway_months} months</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Key Constraint</p>
                    <p className="font-semibold">{ops.financial_reality.key_constraint}</p>
                  </div>
                </div>
                {ops.funding_path && (
                  <p className="mt-3 text-sm text-[#1a73e8] font-medium">
                    Recommended Path: {ops.funding_path}
                  </p>
                )}
              </div>
            )}

            <GroundingBar score={ops.grounding_score || 0.8} />

            {/* Timeline */}
            <div className="mt-6 space-y-4">
              {(ops.roadmap || []).map((phase: any, i: number) => (
                <div key={i} className="card p-5">
                  <div className="flex items-center gap-3 mb-3">
                    <Calendar className="w-5 h-5 text-[#1a73e8]" />
                    <div>
                      <h4 className="font-semibold">{phase.phase}</h4>
                      <p className="text-sm text-gray-500">{phase.title}</p>
                    </div>
                  </div>
                  <ul className="space-y-2">
                    {(phase.tasks || []).map((task: string, j: number) => (
                      <li key={j} className="flex items-start gap-2 text-sm text-gray-700">
                        <CheckSquare className="w-4 h-4 text-gray-300 mt-0.5 flex-shrink-0" />
                        {task}
                      </li>
                    ))}
                  </ul>
                  {phase.milestone && (
                    <p className="mt-2 text-xs text-[#1a73e8] font-medium">
                      Milestone: {phase.milestone}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="card p-8 text-center">
            <div className="text-4xl mb-4 pulse-loading">🗺️</div>
            <p className="text-gray-500">Generating your roadmap...</p>
          </div>
        )}
      </div>
    </div>
  );
}
