import { useState } from "react";
import { X } from "lucide-react";
import type { IdeaIntake } from "../../api/types";

interface Props {
  intake: IdeaIntake;
  onSave: (overrides: Partial<IdeaIntake>) => void;
  onClose: () => void;
}

export default function OverrideModal({ intake, onSave, onClose }: Props) {
  const [form, setForm] = useState<IdeaIntake>({ ...intake });

  const update = (field: keyof IdeaIntake, value: any) =>
    setForm((f) => ({ ...f, [field]: value }));

  const handleSave = () => {
    const changed: any = {};
    for (const key of Object.keys(form) as (keyof IdeaIntake)[]) {
      if (form[key] !== intake[key]) changed[key] = form[key];
    }
    if (Object.keys(changed).length > 0) onSave(changed);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-md max-h-[80vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Update Assumptions</h2>
          <button onClick={onClose}>
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Industry</label>
            <select
              value={form.industry}
              onChange={(e) => update("industry", e.target.value)}
              className="w-full border rounded-lg p-2 text-sm outline-none"
            >
              {["EdTech","FinTech","HealthTech","AgriTech","FoodTech","CleanTech","SaaS","E-Commerce","Logistics","Other"].map(
                (i) => <option key={i}>{i}</option>
              )}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Geography</label>
            <select
              value={form.geography}
              onChange={(e) => update("geography", e.target.value)}
              className="w-full border rounded-lg p-2 text-sm outline-none"
            >
              {["India - Metro","India - Tier 2","India - Tier 3","Global"].map(
                (g) => <option key={g}>{g}</option>
              )}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Target Customer</label>
            <input
              value={form.target_customer}
              onChange={(e) => update("target_customer", e.target.value)}
              className="w-full border rounded-lg p-2 text-sm outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">B2B or B2C</label>
            <div className="flex gap-2">
              {["B2B", "B2C"].map((m) => (
                <button
                  key={m}
                  type="button"
                  onClick={() => update("b2b_or_b2c", m)}
                  className={`flex-1 py-2 rounded-lg border text-sm ${
                    form.b2b_or_b2c === m ? "bg-[#1a73e8] text-white" : ""
                  }`}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={form.has_cofounder}
              onChange={(e) => update("has_cofounder", e.target.checked)}
            />
            <span className="text-sm">Has co-founder</span>
          </div>
        </div>

        <button
          onClick={handleSave}
          className="mt-6 w-full bg-[#1a73e8] text-white py-2.5 rounded-lg font-medium hover:bg-blue-600 transition"
        >
          Save & Re-run Affected Agents
        </button>
      </div>
    </div>
  );
}
