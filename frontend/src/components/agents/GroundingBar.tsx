interface Props {
  score: number;
  label?: string;
}

export default function GroundingBar({ score, label }: Props) {
  const pct = Math.round(score * 100);
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-gray-500">{label || "Grounding"}</span>
      <div className="grounding-bar flex-1">
        <div className="grounding-bar-fill" style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs font-medium">{pct}%</span>
    </div>
  );
}
