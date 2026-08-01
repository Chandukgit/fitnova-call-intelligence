import { useEffect, useState } from "react";
import { PhoneCall, TrendingUp, MessageSquare, Lightbulb } from "lucide-react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import StatCard from "../../components/dashboard/StatCard";
import RecentCallsTable from "../../components/dashboard/RecentCallsTable";
import Card from "../../components/common/Card";
import LoadingSkeleton from "../../components/common/LoadingSkeleton";
import { getCalls, getScores } from "../../services/mockService";

function AdvisorDashboard() {
  const [calls, setCalls] = useState([]);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In this mock, we pretend all calls belong to "Sarah Johnson".
    Promise.all([getCalls(), getScores("call-101")]).then(([callsData, scoreData]) => {
      setCalls(callsData.filter((c) => c.advisorName === "Sarah Johnson"));
      setFeedback(scoreData);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <DashboardLayout role="Advisor">
        <LoadingSkeleton className="h-64 w-full" />
      </DashboardLayout>
    );
  }

  const avgScore = calls.length
    ? Math.round(calls.reduce((sum, c) => sum + c.score, 0) / calls.length)
    : 0;

  return (
    <DashboardLayout role="Advisor">
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">My Dashboard</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">Sarah Johnson · North Region</p>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <StatCard label="My Calls" value={calls.length} icon={PhoneCall} />
        <StatCard label="Average Score" value={avgScore} suffix="%" icon={TrendingUp} />
        <StatCard label="Latest Feedback" value={feedback ? feedback.overallScore : "-"} icon={MessageSquare} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <Card title="Recent Feedback">
          <p className="text-sm text-[var(--color-text)]">{feedback?.summary}</p>
        </Card>

        <Card title="Improvement Tips">
          <ul className="space-y-2">
            {feedback?.recommendations.map((tip, index) => (
              <li key={index} className="flex items-start gap-2 text-sm text-[var(--color-text)]">
                <Lightbulb size={16} className="text-[var(--color-primary)] mt-0.5 shrink-0" />
                <span>{tip}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <Card title="My Calls">
        <RecentCallsTable calls={calls} />
      </Card>
    </DashboardLayout>
  );
}

export default AdvisorDashboard;
