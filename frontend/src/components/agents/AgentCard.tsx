import { RefreshCw, Edit3 } from "lucide-react";
import GroundingBar from "./GroundingBar";

interface Props {
  icon: string;
  title: string;
  status: "pending" | "running" | "completed" | "error" | "stale";
  grounding_score: number;
  scoreLabel: string;
  scoreValue: number;
  sourceDocs: string[];
  children: React.ReactNode;
  onRerun?: () => void;
  onUpdateAssumptions?: () => void;
}

export default function AgentCard({
  icon,
  title,
  status,
  grounding_score,
  scoreLabel,
  scoreValue,
  sourceDocs,
  children,
  onRerun,
  onUpdateAssumptions,
}: Props) {
  if (status === "pending" || status === "running") {
    return (
      <div className="card p-6 agent-card-enter">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-2xl">{icon}</span>
          <h3 className="font-semibold text-lg">{title}</h3>
        </div>
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="h-4 bg-gray-200 rounded pulse-loading"
              style={{ width: `${70 + i * 5}%` }}
            />
          ))}
        </div>
        <p className="text-sm text-gray-400 mt-4">Analyzing...</p>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="card p-6 border-red-200">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-2xl">{icon}</span>
          <h3 className="font-semibold text-lg">{title}</h3>
        </div>
        <p className="text-red-500 text-sm">Agent encountered an error.</p>
        {onRerun && (
          <button
            onClick={onRerun}
            className="mt-3 text-sm text-[#1a73e8] flex items-center gap-1"
          >
            <RefreshCw className="w-3 h-3" /> Retry
          </button>
        )}
      </div>
    );
  }

  return (
    <div
      className={`card p-6 agent-card-enter ${
        status === "stale" ? "card-stale" : ""
      }`}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <h3 className="font-semibold text-lg">{title}</h3>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-500">{scoreLabel}</div>
          <div className="text-xl font-bold text-[#1a73e8]">
            {scoreValue}/10
          </div>
        </div>
      </div>

      {status === "stale" && (
        <div className="bg-yellow-50 text-yellow-700 text-xs px-3 py-1 rounded-full inline-block mb-3">
          Based on old assumptions
        </div>
      )}

      <GroundingBar score={grounding_score} />

      {/* Body */}
      <div className="mt-4">{children}</div>

      {/* Sources */}
      {sourceDocs.length > 0 && (
        <div className="mt-4 pt-3 border-t">
          <p className="text-xs text-gray-400">
            Sources: {sourceDocs.slice(0, 3).join(", ")}
            {sourceDocs.length > 3 && ` +${sourceDocs.length - 3} more`}
          </p>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3 mt-4">
        {onUpdateAssumptions && (
          <button
            onClick={onUpdateAssumptions}
            className="flex items-center gap-1 text-sm text-gray-600 hover:text-[#1a73e8] transition"
          >
            <Edit3 className="w-3 h-3" /> Update Assumptions
          </button>
        )}
        {onRerun && (
          <button
            onClick={onRerun}
            className="flex items-center gap-1 text-sm text-gray-600 hover:text-[#1a73e8] transition"
          >
            <RefreshCw className="w-3 h-3" /> Re-run Agent
          </button>
        )}
      </div>
    </div>
  );
}
