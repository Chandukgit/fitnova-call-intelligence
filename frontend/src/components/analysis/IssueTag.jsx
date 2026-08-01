// A colored tag showing an AI-detected issue or highlight from the call.
const typeColors = {
  positive: "bg-green-100 text-green-700",
  warning: "bg-yellow-100 text-yellow-700",
  critical: "bg-red-100 text-red-700",
};

function IssueTag({ label, type = "warning" }) {
  return (
    <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium mr-2 mb-2 ${typeColors[type]}`}>
      {label}
    </span>
  );
}

export default IssueTag;
