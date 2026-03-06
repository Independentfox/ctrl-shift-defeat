import { CheckCircle, Circle, Lock } from "lucide-react";

interface Props {
  current: "intake" | "ideation" | "execution" | "operation";
  sessionId?: string;
}

const STAGES = [
  { key: "intake", label: "Idea Input" },
  { key: "ideation", label: "Ideation" },
  { key: "execution", label: "Execution" },
  { key: "operation", label: "Operation" },
] as const;

export default function StageProgress({ current }: Props) {
  const currentIdx = STAGES.findIndex((s) => s.key === current);

  return (
    <div className="bg-white border-b px-6 py-4">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <div className="font-bold text-lg text-[#1a73e8]">CO-FOUNDER AI</div>
        <div className="flex items-center gap-2">
          {STAGES.map((stage, i) => {
            const done = i < currentIdx;
            const active = i === currentIdx;
            return (
              <div key={stage.key} className="flex items-center">
                {i > 0 && (
                  <div
                    className={`w-8 h-0.5 ${
                      done ? "bg-[#34a853]" : "bg-gray-200"
                    }`}
                  />
                )}
                <div
                  className={`flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium ${
                    done
                      ? "text-[#34a853]"
                      : active
                      ? "text-[#1a73e8] bg-blue-50"
                      : "text-gray-400"
                  }`}
                >
                  {done ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : active ? (
                    <Circle className="w-4 h-4" />
                  ) : (
                    <Lock className="w-3 h-3" />
                  )}
                  {stage.label}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
