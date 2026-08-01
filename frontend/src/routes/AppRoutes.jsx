import { Routes, Route } from "react-router-dom";

import LoginPage from "../pages/Login/LoginPage";
import DirectorDashboard from "../pages/Director/DirectorDashboard";
import LeaderDashboard from "../pages/Leader/LeaderDashboard";
import AdvisorDashboard from "../pages/Advisor/AdvisorDashboard";
import CallsListPage from "../pages/Shared/CallsListPage";
import CallDetailsPage from "../pages/Shared/CallDetailsPage";
import AnalyticsPage from "../pages/Shared/AnalyticsPage";
import ReportsPage from "../pages/Shared/ReportsPage";
import SettingsPage from "../pages/Shared/SettingsPage";
import NotFoundPage from "../pages/Shared/NotFoundPage";

// All app routes live here, in one simple, readable place.
function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />

      <Route path="/director" element={<DirectorDashboard />} />
      <Route path="/leader" element={<LeaderDashboard />} />
      <Route path="/advisor" element={<AdvisorDashboard />} />

      <Route path="/calls" element={<CallsListPage />} />
      <Route path="/calls/:callId" element={<CallDetailsPage />} />
      <Route path="/analytics" element={<AnalyticsPage />} />
      <Route path="/reports" element={<ReportsPage />} />
      <Route path="/settings" element={<SettingsPage />} />

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default AppRoutes;
