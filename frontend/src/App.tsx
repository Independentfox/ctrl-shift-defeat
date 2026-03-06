import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import IdeaIntakePage from "./pages/IdeaIntakePage";
import IdeationDashboard from "./pages/IdeationDashboard";
import ExecutionDashboard from "./pages/ExecutionDashboard";
import OperationDashboard from "./pages/OperationDashboard";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/app" element={<IdeaIntakePage />} />
      <Route path="/session/:id/ideation" element={<IdeationDashboard />} />
      <Route path="/session/:id/execution" element={<ExecutionDashboard />} />
      <Route path="/session/:id/operation" element={<OperationDashboard />} />
    </Routes>
  );
}
