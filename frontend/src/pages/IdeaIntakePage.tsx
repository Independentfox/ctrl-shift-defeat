import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createSession, runStage } from "../api/client";
import type { IdeaIntake } from "../api/types";
import StageProgress from "../components/layout/StageProgress";

const INDUSTRIES = [
  "EdTech", "FinTech", "HealthTech", "AgriTech", "FoodTech",
  "CleanTech", "SaaS", "E-Commerce", "Logistics", "Other",
];

export default function IdeaIntakePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState<IdeaIntake>({
    raw_idea: "",
    industry: "EdTech",
    stage: "Idea",
    team_size: 1,
    geography: "India - Tier 2",
    budget_range: "< 5L",
    target_customer: "",
    b2b_or_b2c: "B2C",
    has_cofounder: false,
  });

  const update = (field: keyof IdeaIntake, value: any) =>
    setForm((f) => ({ ...f, [field]: value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.raw_idea.trim()) return;
    setLoading(true);
    try {
      const sessionId = await createSession(form);
      await runStage(sessionId, "ideation");
      navigate(`/session/${sessionId}/ideation`);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f8f9fa]">
      <StageProgress current="intake" />
      <div className="max-w-2xl mx-auto py-10 px-6">
        <h1 className="text-3xl font-bold mb-2">Describe Your Startup Idea</h1>
        <p className="text-gray-600 mb-8">
          Our 4 AI agents will stress-test it against real startup data.
        </p>

        <form onSubmit={handleSubmit} className="card p-8 space-y-6">
          {/* Raw Idea */}
          <div>
            <label className="block text-sm font-medium mb-1">
              Your Idea *
            </label>
            <textarea
              value={form.raw_idea}
              onChange={(e) => update("raw_idea", e.target.value)}
              placeholder="Describe your startup idea in 2-3 sentences..."
              className="w-full border rounded-lg p-3 h-28 resize-none focus:ring-2 focus:ring-[#1a73e8] focus:border-transparent outline-none"
              required
            />
          </div>

          {/* Industry + Stage */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Industry</label>
              <select
                value={form.industry}
                onChange={(e) => update("industry", e.target.value)}
                className="w-full border rounded-lg p-2.5 outline-none"
              >
                {INDUSTRIES.map((i) => (
                  <option key={i}>{i}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Stage</label>
              <select
                value={form.stage}
                onChange={(e) => update("stage", e.target.value)}
                className="w-full border rounded-lg p-2.5 outline-none"
              >
                <option>Idea</option>
                <option>MVP</option>
                <option>Early Revenue</option>
              </select>
            </div>
          </div>

          {/* Geography + Budget */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Geography</label>
              <select
                value={form.geography}
                onChange={(e) => update("geography", e.target.value)}
                className="w-full border rounded-lg p-2.5 outline-none"
              >
                <option>India - Metro</option>
                <option>India - Tier 2</option>
                <option>India - Tier 3</option>
                <option>Global</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Budget Range</label>
              <select
                value={form.budget_range}
                onChange={(e) => update("budget_range", e.target.value)}
                className="w-full border rounded-lg p-2.5 outline-none"
              >
                <option>{"< 5L"}</option>
                <option>5-25L</option>
                <option>25L+</option>
              </select>
            </div>
          </div>

          {/* Target Customer + B2B/B2C */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                Target Customer
              </label>
              <input
                value={form.target_customer}
                onChange={(e) => update("target_customer", e.target.value)}
                placeholder="e.g., College students"
                className="w-full border rounded-lg p-2.5 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Model</label>
              <div className="flex gap-2 mt-1">
                {["B2B", "B2C"].map((m) => (
                  <button
                    key={m}
                    type="button"
                    onClick={() => update("b2b_or_b2c", m)}
                    className={`flex-1 py-2 rounded-lg border text-sm font-medium transition ${
                      form.b2b_or_b2c === m
                        ? "bg-[#1a73e8] text-white border-[#1a73e8]"
                        : "bg-white text-gray-600"
                    }`}
                  >
                    {m}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Team Size + Cofounder */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Team Size</label>
              <input
                type="number"
                min={1}
                max={20}
                value={form.team_size}
                onChange={(e) => update("team_size", +e.target.value)}
                className="w-full border rounded-lg p-2.5 outline-none"
              />
            </div>
            <div className="flex items-end">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={form.has_cofounder}
                  onChange={(e) => update("has_cofounder", e.target.checked)}
                  className="w-4 h-4"
                />
                <span className="text-sm">I have a co-founder</span>
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !form.raw_idea.trim()}
            className="w-full gradient-bg text-white py-3 rounded-lg font-semibold text-lg hover:opacity-90 transition disabled:opacity-50"
          >
            {loading ? "Analyzing..." : "Stress-Test My Idea"}
          </button>
        </form>
      </div>
    </div>
  );
}
