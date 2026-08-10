import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import CallVolumeChart from "../../components/charts/CallVolumeChart";
import ScoreTrendChart from "../../components/charts/ScoreTrendChart";
import TeamComparisonChart from "../../components/charts/TeamComparisonChart";
import ComplianceChart from "../../components/charts/ComplianceChart";
import LoadingSkeleton from "../../components/common/LoadingSkeleton";
import { getAnalytics } from "../../services/fitnovaService";

function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getAnalytics().then(setAnalytics).catch(() => setError("Unable to load analytics.")).finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <LoadingSkeleton className="h-64 w-full" />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">Analytics</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">
        Overall call performance across the organization.
      </p>
      {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <CallVolumeChart data={analytics.weeklyCallVolume} />
        <ScoreTrendChart data={analytics.scoreTrend} />
        <TeamComparisonChart data={analytics.teamComparison} />
        <ComplianceChart data={analytics.complianceBreakdown} />
      </div>
    </DashboardLayout>
  );
}

export default AnalyticsPage;
