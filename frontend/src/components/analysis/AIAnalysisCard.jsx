import Card from "../common/Card";
import { getScoreColor } from "../../utils/helpers";

// Displays the AI-generated score breakdown and summary for a call.
function AIAnalysisCard({ analysis }) {
  if (!analysis) return null;

  const metrics = [
    { label: "Communication", value: analysis.communication },
    { label: "Compliance", value: analysis.compliance },
    { label: "Product Knowledge", value: analysis.productKnowledge },
    { label: "Customer Satisfaction", value: analysis.customerSatisfaction },
  ];

  return (
    <Card title="AI Analysis">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-[var(--color-text-soft)]">Overall Score</p>
        <p className={`text-2xl font-bold ${getScoreColor(analysis.overallScore)}`}>
          {analysis.overallScore}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        {metrics.map((m) => (
          <div key={m.label}>
            <p className="text-xs text-[var(--color-text-soft)] mb-1">{m.label}</p>
            <p className={`text-sm font-semibold ${m.value == null ? "text-[var(--color-text-soft)]" : getScoreColor(m.value)}`}>{m.value ?? "—"}</p>
          </div>
        ))}
      </div>

      <p className="text-sm text-[var(--color-text)] mb-3">{analysis.summary}</p>
    </Card>
  );
}

export default AIAnalysisCard;
