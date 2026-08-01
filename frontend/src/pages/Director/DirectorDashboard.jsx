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
import { getOrganization, getTeams, getAdvisors, getCalls, getAnalytics } from "../../services/mockService";

function DirectorDashboard() {
  const [org, setOrg] = useState(null);
  const [teams, setTeams] = useState([]);
  const [advisors, setAdvisors] = useState([]);
  const [calls, setCalls] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load all the mock data needed for this dashboard.
    Promise.all([getOrganization(), getTeams(), getAdvisors(), getCalls(), getAnalytics()]).then(
      ([orgData, teamsData, advisorsData, callsData, analyticsData]) => {
        setOrg(orgData);
        setTeams(teamsData);
        setAdvisors(advisorsData);
        setCalls(callsData);
        setAnalytics(analyticsData);
        setLoading(false);
      }
    );
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
        <StatCard label="Total Calls" value={org.totalCallsThisMonth} icon={PhoneCall} />
        <StatCard label="Average Score" value={82} suffix="%" icon={TrendingUp} />
        <StatCard label="Compliance" value={91} suffix="%" icon={ShieldCheck} />
        <StatCard label="Teams" value={org.totalTeams} icon={Users} />
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
