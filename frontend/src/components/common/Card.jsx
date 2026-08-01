// A simple card wrapper used all over the dashboards.
function Card({ children, className = "", title }) {
  return (
    <div
      className={`bg-[var(--color-card)] border border-[var(--color-border)] rounded-xl p-5 shadow-sm ${className}`}
    >
      {title && <h3 className="text-sm font-semibold text-[var(--color-text)] mb-3">{title}</h3>}
      {children}
    </div>
  );
}

export default Card;
