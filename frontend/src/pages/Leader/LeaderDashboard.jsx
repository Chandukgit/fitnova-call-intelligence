import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import StatCard from "../../components/dashboard/StatCard";
import RecentCallsTable from "../../components/dashboard/RecentCallsTable";
import TeamComparisonChart from "../../components/charts/TeamComparisonChart";
import Card from "../../components/common/Card";
import Table from "../../components/common/Table";
import LoadingSkeleton from "../../components/common/LoadingSkeleton";
import { Users, Star, PhoneCall, ClipboardList } from "lucide-react";
import { getAdvisors, getCallData, getAnalytics, getAnalysesRaw, getTeams } from "../../services/fitnovaService";

function LeaderDashboard() {
  const [advisors, setAdvisors] = useState([]);
  const [calls, setCalls] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getAdvisors(), getCallData(), getAnalytics(), getAnalysesRaw(), getTeams()]).then(
      ([advisorsData, callsData, analyticsData, analyses, teams]) => {
        setAdvisors(advisorsData.map((advisor) => ({ ...advisor, name: `${advisor.first_name} ${advisor.last_name}`, totalCalls: callsData.filter((call) => call.advisor_id === advisor.id).length, avgScore: Math.round(analyses.filter((analysis) => callsData.find((call) => call.id === analysis.call_id)?.advisor_id === advisor.id).reduce((sum, analysis) => sum + (analysis.overall_score || 0), 0) / Math.max(1, analyses.filter((analysis) => callsData.find((call) => call.id === analysis.call_id)?.advisor_id === advisor.id).length)), team: teams.find((team) => team.id === advisor.team_id)?.name || "—" })));
        setCalls(callsData);
        setAnalytics(analyticsData);
      }).finally(() => setLoading(false));
  }, []);

  const ranking = [...advisors].sort((a, b) => b.avgScore - a.avgScore);
  const pendingReviews = calls.filter((c) => c.status !== "COMPLETED");

  if (loading) {
    return (
      <DashboardLayout role="Team Leader">
        <LoadingSkeleton className="h-64 w-full" />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout role="Team Leader">
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">Team Overview</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">North Region</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Team Members" value={advisors.length} icon={Users} />
        <StatCard label="Team Avg Score" value={analytics.scoreTrend[0]?.avgScore || 0} suffix="%" icon={Star} />
        <StatCard label="Calls This Week" value={calls.length} icon={PhoneCall} />
        <StatCard label="Pending Reviews" value={pendingReviews.length} icon={ClipboardList} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <TeamComparisonChart data={analytics.teamComparison} />

        <Card title="Advisor Ranking">
          <Table
            columns={[
              { header: "Rank", accessor: "rank" },
              { header: "Name", accessor: "name" },
              { header: "Avg Score", accessor: "avgScore" },
              { header: "Calls", accessor: "totalCalls" },
            ]}
            data={ranking.map((a, i) => ({ ...a, rank: i + 1 }))}
          />
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Recent Calls">
          <RecentCallsTable calls={calls} />
        </Card>

        <Card title="Pending Reviews">
          <RecentCallsTable calls={pendingReviews} />
        </Card>
      </div>
    </DashboardLayout>
  );
}

export default LeaderDashboard;
