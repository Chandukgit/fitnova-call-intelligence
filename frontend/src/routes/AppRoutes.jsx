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
import UploadPage from "../pages/Shared/UploadPage";
import ProtectedRoute from "./ProtectedRoute";

// All app routes live here, in one simple, readable place.
function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />

      <Route path="/director" element={<ProtectedRoute roles={["ADMIN"]}><DirectorDashboard /></ProtectedRoute>} />
      <Route path="/leader" element={<ProtectedRoute roles={["MANAGER"]}><LeaderDashboard /></ProtectedRoute>} />
      <Route path="/advisor" element={<ProtectedRoute roles={["ADVISOR"]}><AdvisorDashboard /></ProtectedRoute>} />

      <Route path="/calls" element={<ProtectedRoute><CallsListPage /></ProtectedRoute>} />
      <Route path="/calls/:callId" element={<ProtectedRoute><CallDetailsPage /></ProtectedRoute>} />
      <Route path="/upload" element={<ProtectedRoute><UploadPage /></ProtectedRoute>} />
      <Route path="/analytics" element={<ProtectedRoute><AnalyticsPage /></ProtectedRoute>} />
      <Route path="/reports" element={<ProtectedRoute><ReportsPage /></ProtectedRoute>} />
      <Route path="/settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default AppRoutes;
