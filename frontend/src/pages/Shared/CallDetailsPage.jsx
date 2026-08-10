import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import DashboardLayout from "../../components/layout/DashboardLayout";
import Card from "../../components/common/Card";
import LoadingSkeleton from "../../components/common/LoadingSkeleton";
import AudioPlayerPlaceholder from "../../components/upload/AudioPlayerPlaceholder";
import TranscriptList from "../../components/transcript/TranscriptList";
import AIAnalysisCard from "../../components/analysis/AIAnalysisCard";
import RecommendationsList from "../../components/analysis/RecommendationsList";
import IssueTag from "../../components/analysis/IssueTag";
import { getCallDetails } from "../../services/fitnovaService";

function CallDetailsPage() {
  const { callId } = useParams();
  const [call, setCall] = useState(null);
  const [transcript, setTranscript] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    getCallDetails(callId).then((data) => {
      if (!data) return;
      setCall(data.call);
      setTranscript(data.transcript);
      setAnalysis(data.analysis);
      setTags(data.tags);
      setFeedback(data.feedback);
    }).catch(() => setError("Unable to load this call.")).finally(() => setLoading(false));
  }, [callId]);

  if (loading) {
    return (
      <DashboardLayout>
        <LoadingSkeleton className="h-64 w-full" />
      </DashboardLayout>
    );
  }

  if (!call) {
    return (
      <DashboardLayout>
        <p className="text-sm text-[var(--color-text-soft)]">Call not found.</p>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">{call.original_filename}</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">
        {call.customer ? `${call.customer.first_name} ${call.customer.last_name}` : "Unknown customer"} · {new Date(call.created_at).toLocaleDateString()}
      </p>

      {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

      <div className="mb-6">
        <AudioPlayerPlaceholder duration={call.duration_seconds ? `${call.duration_seconds}s` : "—"} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <Card title="Customer Information">
          <p className="text-sm text-[var(--color-text)]">Name: {call.customer ? `${call.customer.first_name} ${call.customer.last_name}` : "Unknown"}</p>
          <p className="text-sm text-[var(--color-text)] mt-1">Language: {call.language || "Not detected"}</p>
        </Card>

        <Card title="Advisor Information">
          <p className="text-sm text-[var(--color-text)]">Name: {call.advisor ? `${call.advisor.first_name} ${call.advisor.last_name}` : "Unknown"}</p>
          <p className="text-sm text-[var(--color-text)] mt-1">Score: {analysis?.overallScore ?? "Not analyzed"}</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <TranscriptList messages={transcript} />

        <div className="space-y-4">
          <AIAnalysisCard analysis={analysis} />
          <RecommendationsList recommendations={analysis?.recommendations} />
        </div>
      </div>

      <Card title="Issue Tags">
        {tags.length === 0 ? (
          <p className="text-sm text-[var(--color-text-soft)]">No issues detected for this call.</p>
        ) : (
          <div>
            {tags.map((tag) => (
              <IssueTag key={tag.id} label={tag.issue_type} type={tag.severity === "CRITICAL" ? "critical" : tag.severity === "HIGH" ? "warning" : "positive"} />
            ))}
          </div>
        )}
      </Card>

      <Card title="Feedback" className="mt-6">
        {feedback.length ? feedback.map((item) => <p key={item.id} className="text-sm text-[var(--color-text)] mb-2">{item.reviewer_comment || item.advisor_comment}</p>) : <p className="text-sm text-[var(--color-text-soft)]">No feedback available for this call.</p>}
      </Card>
    </DashboardLayout>
  );
}

export default CallDetailsPage;
