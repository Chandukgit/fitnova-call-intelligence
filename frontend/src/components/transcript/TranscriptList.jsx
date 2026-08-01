import Card from "../common/Card";
import TranscriptMessage from "./TranscriptMessage";

// Renders the full transcript for a call.
function TranscriptList({ messages }) {
  return (
    <Card title="Transcript">
      {messages.length === 0 ? (
        <p className="text-sm text-[var(--color-text-soft)]">No transcript available for this call.</p>
      ) : (
        <div className="max-h-96 overflow-y-auto pr-2">
          {messages.map((msg, index) => (
            <TranscriptMessage key={index} {...msg} />
          ))}
        </div>
      )}
    </Card>
  );
}

export default TranscriptList;
