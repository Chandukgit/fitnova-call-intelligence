// A single line in the call transcript.
// speaker is either "advisor" or "customer" and changes the alignment/color.
function TranscriptMessage({ speaker, time, text }) {
  const isAdvisor = speaker === "advisor";

  return (
    <div className={`flex ${isAdvisor ? "justify-start" : "justify-end"} mb-3`}>
      <div
        className={`max-w-[75%] px-4 py-2 rounded-xl text-sm ${
          isAdvisor
            ? "bg-[var(--color-primary-light)] text-[var(--color-text)]"
            : "bg-gray-100 text-[var(--color-text)]"
        }`}
      >
        <p className="text-xs font-semibold mb-1 text-[var(--color-text-soft)]">
          {isAdvisor ? "Advisor" : "Customer"} · {time}
        </p>
        <p>{text}</p>
      </div>
    </div>
  );
}

export default TranscriptMessage;
