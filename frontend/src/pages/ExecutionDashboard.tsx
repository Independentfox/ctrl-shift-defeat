import { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getSessionOutput, getDownloadUrl, runStage } from "../api/client";
import type { StartupContext } from "../api/types";
import StageProgress from "../components/layout/StageProgress";
import GroundingBar from "../components/agents/GroundingBar";
import { Download, FileText, DollarSign } from "lucide-react";

export default function ExecutionDashboard() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
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

  const handleDownload = async (fileType: string) => {
    if (!id) return;
    const url = await getDownloadUrl(id, fileType);
    window.open(url, "_blank");
  };

  const handleProceed = async () => {
    if (!id) return;
    await runStage(id, "operation");
    navigate(`/session/${id}/operation`);
  };

  const pitch = ctx?.execution_outputs?.pitch_deck;
  const financial = ctx?.execution_outputs?.financial_model;

  return (
    <div className="min-h-screen bg-[#f8f9fa]">
      <StageProgress current="execution" />
      <div className="max-w-4xl mx-auto py-8 px-6">
        <h1 className="text-2xl font-bold mb-6">Execution Artifacts</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Pitch Deck */}
          <div className="card p-6">
            <div className="flex items-center gap-3 mb-4">
              <FileText className="w-8 h-8 text-[#1a73e8]" />
              <div>
                <h3 className="font-semibold text-lg">Pitch Deck</h3>
                <p className="text-sm text-gray-500">
                  {pitch?.slides_generated || 12} slides |{" "}
                  {pitch?.evidence_citations || 0} citations
                </p>
              </div>
            </div>

            {pitch?.status === "completed" ? (
              <>
                <GroundingBar score={pitch.grounding_score || 0.83} />
                <div className="mt-4 space-y-2">
                  {pitch.slides?.slice(0, 4).map((s: any) => (
                    <div key={s.slide_number} className="flex items-center gap-2 text-sm">
                      <span className="w-6 h-6 bg-blue-50 text-[#1a73e8] rounded flex items-center justify-center text-xs font-bold">
                        {s.slide_number}
                      </span>
                      <span className="text-gray-700">{s.title}</span>
                    </div>
                  ))}
                  {(pitch.slides?.length || 0) > 4 && (
                    <p className="text-xs text-gray-400">+{pitch.slides.length - 4} more slides</p>
                  )}
                </div>
                <button
                  onClick={() => handleDownload("pitch_deck")}
                  className="mt-4 w-full flex items-center justify-center gap-2 bg-[#1a73e8] text-white py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition"
                >
                  <Download className="w-4 h-4" /> Download PPTX
                </button>
              </>
            ) : (
              <div className="space-y-2 mt-4">
                {[1,2,3].map(i => (
                  <div key={i} className="h-4 bg-gray-200 rounded pulse-loading" style={{width: `${60+i*10}%`}} />
                ))}
                <p className="text-sm text-gray-400 mt-2">Generating...</p>
              </div>
            )}
          </div>

          {/* Financial Model */}
          <div className="card p-6">
            <div className="flex items-center gap-3 mb-4">
              <DollarSign className="w-8 h-8 text-[#34a853]" />
              <div>
                <h3 className="font-semibold text-lg">Financial Model</h3>
                <p className="text-sm text-gray-500">Comparable company data</p>
              </div>
            </div>

            {financial?.status === "completed" ? (
              <>
                <GroundingBar score={financial.grounding_score || 0.88} />
                <div className="mt-4 space-y-3 text-sm">
                  {financial.data?.cost_structure?.total_burn && (
                    <div>
                      <p className="text-xs text-gray-500">Monthly Burn</p>
                      <p className="font-semibold">{financial.data.cost_structure.total_burn}</p>
                    </div>
                  )}
                  {financial.data?.funding_analysis?.recommended_raise && (
                    <div>
                      <p className="text-xs text-gray-500">Recommended Raise</p>
                      <p className="font-semibold">{financial.data.funding_analysis.recommended_raise}</p>
                    </div>
                  )}
                  {financial.data?.funding_analysis?.runway_without_funding_months && (
                    <div>
                      <p className="text-xs text-gray-500">Runway</p>
                      <p className="font-semibold">{financial.data.funding_analysis.runway_without_funding_months} months</p>
                    </div>
                  )}
                </div>
                <button
                  onClick={() => handleDownload("financial_model")}
                  className="mt-4 w-full flex items-center justify-center gap-2 bg-[#34a853] text-white py-2 rounded-lg text-sm font-medium hover:bg-green-600 transition"
                >
                  <Download className="w-4 h-4" /> Download Excel
                </button>
              </>
            ) : (
              <div className="space-y-2 mt-4">
                {[1,2,3].map(i => (
                  <div key={i} className="h-4 bg-gray-200 rounded pulse-loading" style={{width: `${60+i*10}%`}} />
                ))}
                <p className="text-sm text-gray-400 mt-2">Calculating...</p>
              </div>
            )}
          </div>
        </div>

        <button
          onClick={handleProceed}
          disabled={pitch?.status !== "completed" || financial?.status !== "completed"}
          className="mt-8 w-full gradient-bg text-white py-3 rounded-lg font-semibold text-lg hover:opacity-90 transition disabled:opacity-50"
        >
          Proceed to Operations Roadmap
        </button>
      </div>
    </div>
  );
}
