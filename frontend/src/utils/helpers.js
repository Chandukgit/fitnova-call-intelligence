// Small helper functions used across the app.
// Kept simple on purpose - no advanced abstractions.

// Turns "2024-05-01" into "May 1, 2024"
export function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

// Returns a tailwind color class based on a score out of 100
export function getScoreColor(score) {
  if (score >= 80) return "text-green-600";
  if (score >= 60) return "text-yellow-600";
  return "text-red-600";
}

// Returns a background color class for badges based on status
export function getStatusColor(status) {
  switch (status) {
    case "Completed":
      return "bg-green-100 text-green-700";
    case "Pending":
      return "bg-yellow-100 text-yellow-700";
    case "Flagged":
      return "bg-red-100 text-red-700";
    default:
      return "bg-gray-100 text-gray-700";
  }
}

// Shortens long text and adds "..."
export function truncateText(text, maxLength = 60) {
  if (!text) return "";
  return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
}
