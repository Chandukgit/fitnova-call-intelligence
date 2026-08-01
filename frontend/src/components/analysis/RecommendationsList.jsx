import { CheckCircle2 } from "lucide-react";
import Card from "../common/Card";

// Shows AI recommendations for the advisor to improve.
function RecommendationsList({ recommendations = [] }) {
  return (
    <Card title="Recommendations">
      {recommendations.length === 0 ? (
        <p className="text-sm text-[var(--color-text-soft)]">No recommendations for this call.</p>
      ) : (
        <ul className="space-y-2">
          {recommendations.map((tip, index) => (
            <li key={index} className="flex items-start gap-2 text-sm text-[var(--color-text)]">
              <CheckCircle2 size={16} className="text-[var(--color-primary)] mt-0.5 shrink-0" />
              <span>{tip}</span>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}

export default RecommendationsList;
