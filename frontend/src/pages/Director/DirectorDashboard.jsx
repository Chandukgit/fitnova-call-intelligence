import { useEffect, useState } from "react";
import { PhoneCall, TrendingUp, ShieldCheck, Users } from "lucide-react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import StatCard from "../../components/dashboard/StatCard";
import RecentCallsTable from "../../components/dashboard/RecentCallsTable";
import CallVolumeChart from "../../components/charts/CallVolumeChart";
import ScoreTrendChart from "../../components/charts/ScoreTrendChart";
import Card from "../../components/common/Card";
import Table from "../../components/common/Table";
import LoadingSkeleton from "../../components/common/LoadingSkeleton";
import { getOrganizations, getTeams, getAdvisors, getCallData, getAnalytics, getAnalysesRaw } from "../../services/fitnovaService";

function DirectorDashboard() {
  const [org, setOrg] = useState(null);
  const [teams, setTeams] = useState([]);
  const [advisors, setAdvisors] = useState([]);
  const [calls, setCalls] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getOrganizations(), getTeams(), getAdvisors(), getCallData(), getAnalytics(), getAnalysesRaw()]).then(
      ([organizations, teamsData, advisorsData, callsData, analyticsData, analyses]) => {
        setOrg(organizations[0] || { name: "No organization" });
        setTeams(teamsData.map((team) => ({ ...team, advisors: advisorsData.filter((advisor) => advisor.team_id === team.id).length, avgScore: 0, leader: "—" })));
        setAdvisors(advisorsData.map((advisor) => ({ ...advisor, name: `${advisor.first_name} ${advisor.last_name}`, team: teamsData.find((team) => team.id === advisor.team_id)?.name || "—", avgScore: Math.round((analyses.filter((analysis) => callsData.find((call) => call.id === analysis.call_id)?.advisor_id === advisor.id).reduce((sum, analysis) => sum + (analysis.overall_score || 0), 0) / Math.max(1, analyses.filter((analysis) => callsData.find((call) => call.id === analysis.call_id)?.advisor_id === advisor.id).length))) })));
        setCalls(callsData);
        setAnalytics(analyticsData);
      }).finally(() => setLoading(false));
  }, []);

  const topAdvisors = [...advisors].sort((a, b) => b.avgScore - a.avgScore).slice(0, 5);

  if (loading) {
    return (
      <DashboardLayout role="Sales Director">
        <LoadingSkeleton className="h-64 w-full" />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout role="Sales Director">
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">Director Overview</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">{org.name}</p>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total Calls" value={calls.length} icon={PhoneCall} />
        <StatCard label="Average Score" value={analytics.scoreTrend[0]?.avgScore || 0} suffix="%" icon={TrendingUp} />
        <StatCard label="Completed Calls" value={calls.filter((call) => call.status === "COMPLETED").length} icon={ShieldCheck} />
        <StatCard label="Teams" value={teams.length} icon={Users} />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <CallVolumeChart data={analytics.weeklyCallVolume} />
        <ScoreTrendChart data={analytics.scoreTrend} />
      </div>

      {/* Teams + Top Advisors */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <Card title="Teams">
          <Table
            columns={[
              { header: "Team", accessor: "name" },
              { header: "Leader", accessor: "leader" },
              { header: "Advisors", accessor: "advisors" },
              { header: "Avg Score", accessor: "avgScore" },
            ]}
            data={teams}
          />
        </Card>

        <Card title="Top Advisors">
          <Table
            columns={[
              { header: "Name", accessor: "name" },
              { header: "Team", accessor: "team" },
              { header: "Avg Score", accessor: "avgScore" },
              { header: "Compliance", accessor: "compliance" },
            ]}
            data={topAdvisors}
          />
        </Card>
      </div>

      {/* Recent Calls */}
      <Card title="Recent Calls">
        <RecentCallsTable calls={calls} />
      </Card>
    </DashboardLayout>
  );
}

export default DirectorDashboard;
