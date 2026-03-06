import { useNavigate } from "react-router-dom";
import { Rocket, Shield, BarChart3, Users } from "lucide-react";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen">
      {/* Hero */}
      <div className="gradient-bg text-white py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-4">CO-FOUNDER AI</h1>
          <p className="text-xl mb-2 opacity-90">
            Multi-Agent Founding Intelligence System
          </p>
          <p className="text-lg mb-8 opacity-75">
            Stress-test your startup idea with real data — not AI guesses
          </p>
          <button
            onClick={() => navigate("/app")}
            className="bg-white text-[#1a73e8] px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-100 transition"
          >
            Validate Your Idea
          </button>
        </div>
      </div>

      {/* Features */}
      <div className="max-w-6xl mx-auto py-16 px-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          {
            icon: Shield,
            title: "Shark Tank Agent",
            desc: "Compare against 700+ real pitch outcomes",
          },
          {
            icon: BarChart3,
            title: "VC Agent",
            desc: "Benchmark against 5,000+ YC companies",
          },
          {
            icon: Users,
            title: "Consultant Agent",
            desc: "Verified market data from Crunchbase",
          },
          {
            icon: Rocket,
            title: "Customer Agent",
            desc: "Objections from 500+ failure post-mortems",
          },
        ].map((f) => (
          <div key={f.title} className="card p-6 text-center">
            <f.icon className="w-10 h-10 mx-auto mb-3 text-[#1a73e8]" />
            <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
            <p className="text-gray-600 text-sm">{f.desc}</p>
          </div>
        ))}
      </div>

      {/* How It Works */}
      <div className="bg-white py-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-8">3-Stage Validation</h2>
          <div className="flex flex-col md:flex-row justify-center gap-8">
            {[
              { step: "1", title: "Ideation", desc: "4 agents stress-test your idea" },
              { step: "2", title: "Execution", desc: "Pitch deck + financial model" },
              { step: "3", title: "Operation", desc: "Constraint-driven roadmap" },
            ].map((s) => (
              <div key={s.step} className="flex-1">
                <div className="w-12 h-12 rounded-full gradient-bg text-white flex items-center justify-center text-xl font-bold mx-auto mb-3">
                  {s.step}
                </div>
                <h3 className="font-semibold text-lg">{s.title}</h3>
                <p className="text-gray-600 text-sm mt-1">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
