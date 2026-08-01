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
import { getCallById, getTranscript, getScores, getIssueTags } from "../../services/mockService";

function CallDetailsPage() {
  const { callId } = useParams();
  const [call, setCall] = useState(null);
  const [transcript, setTranscript] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      getCallById(callId),
      getTranscript(callId),
      getScores(callId),
      getIssueTags(callId),
    ]).then(([callData, transcriptData, scoreData, tagData]) => {
      setCall(callData);
      setTranscript(transcriptData);
      setAnalysis(scoreData);
      setTags(tagData);
      setLoading(false);
    });
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
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">{call.topic}</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">
        {call.customerName} · {call.date} · {call.duration}
      </p>

      <div className="mb-6">
        <AudioPlayerPlaceholder duration={call.duration} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <Card title="Customer Information">
          <p className="text-sm text-[var(--color-text)]">Name: {call.customerName}</p>
          <p className="text-sm text-[var(--color-text)] mt-1">Topic: {call.topic}</p>
        </Card>

        <Card title="Advisor Information">
          <p className="text-sm text-[var(--color-text)]">Name: {call.advisorName}</p>
          <p className="text-sm text-[var(--color-text)] mt-1">Score: {call.score}</p>
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
              <IssueTag key={tag.id} label={tag.label} type={tag.type} />
            ))}
          </div>
        )}
      </Card>
    </DashboardLayout>
  );
}

export default CallDetailsPage;
