import { CheckCircle, AlertTriangle } from "lucide-react";

interface Props {
  data: {
    overall_viability_score: number;
    top_strengths: string[];
    top_risks: string[];
    proceed_to_execution: boolean;
    recommendation?: string;
  } | null;
  onProceed: () => void;
}

export default function SynthesisCard({ data, onProceed }: Props) {
  if (!data) return null;

  return (
    <div className="card p-6 agent-card-enter mt-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🧠</span>
          <h3 className="font-semibold text-lg">Ideation Synthesis</h3>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-500">Viability</div>
          <div className="text-2xl font-bold text-[#1a73e8]">
            {data.overall_viability_score}/10
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mt-4">
        <div>
          <h4 className="font-medium text-sm mb-2 flex items-center gap-1">
            <CheckCircle className="w-4 h-4 text-green-500" /> Top Strengths
          </h4>
          <ul className="space-y-1">
            {data.top_strengths.map((s, i) => (
              <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                <span className="text-green-500 mt-0.5">+</span> {s}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h4 className="font-medium text-sm mb-2 flex items-center gap-1">
            <AlertTriangle className="w-4 h-4 text-yellow-500" /> Top Risks
          </h4>
          <ul className="space-y-1">
            {data.top_risks.map((r, i) => (
              <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                <span className="text-yellow-500 mt-0.5">!</span> {r}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {data.recommendation && (
        <p className="text-sm text-gray-600 mt-4 italic">
          {data.recommendation}
        </p>
      )}

      <button
        onClick={onProceed}
        className="mt-6 w-full gradient-bg text-white py-3 rounded-lg font-semibold hover:opacity-90 transition"
      >
        {data.proceed_to_execution
          ? "Proceed to Execution"
          : "Update My Idea First"}
      </button>
    </div>
  );
}
