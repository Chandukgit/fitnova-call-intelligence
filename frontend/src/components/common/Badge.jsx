// Small colored label, used for status and roles.
function Badge({ children, colorClass = "bg-gray-100 text-gray-700" }) {
  return (
    <span className={`inline-block px-2.5 py-1 rounded-full text-xs font-medium ${colorClass}`}>
      {children}
    </span>
  );
}

export default Badge;
