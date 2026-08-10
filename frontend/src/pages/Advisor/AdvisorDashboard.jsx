import { useEffect, useState } from "react";
import { PhoneCall, TrendingUp, MessageSquare, Lightbulb } from "lucide-react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import StatCard from "../../components/dashboard/StatCard";
import RecentCallsTable from "../../components/dashboard/RecentCallsTable";
import Card from "../../components/common/Card";
import LoadingSkeleton from "../../components/common/LoadingSkeleton";
import { getCallData, getAnalysesRaw, getStoredUser } from "../../services/fitnovaService";

function AdvisorDashboard() {
  const [calls, setCalls] = useState([]);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const user = getStoredUser();
    Promise.all([getCallData(), getAnalysesRaw()]).then(([callsData, analyses]) => {
      const myCalls = callsData.filter((call) => call.advisor_id === user?.advisor_id);
      setCalls(myCalls);
      const latest = analyses.filter((analysis) => myCalls.some((call) => call.id === analysis.call_id)).sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0];
      setFeedback(latest && { ...latest, overallScore: latest.overall_score, recommendations: latest.recommendation ? latest.recommendation.split("\n") : [] });
    }).finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <DashboardLayout role="Advisor">
        <LoadingSkeleton className="h-64 w-full" />
      </DashboardLayout>
    );
  }

  const callsWithScore = calls.filter((c) => typeof c.score === "number" && c.score !== null);
  const avgScore = callsWithScore.length
    ? Math.round(callsWithScore.reduce((sum, c) => sum + c.score, 0) / callsWithScore.length)
    : 0;

  return (
    <DashboardLayout role="Advisor">
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">My Dashboard</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">Your recent call performance.</p>

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
            {(feedback?.recommendations || []).map((tip, index) => (
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
