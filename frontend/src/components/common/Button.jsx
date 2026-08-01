// A simple, reusable button.
// variant can be "primary", "outline", or "ghost".
function Button({ children, onClick, variant = "primary", type = "button", className = "" }) {
  const baseStyles = "px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150";

  const variants = {
    primary: "bg-[var(--color-primary)] text-white hover:bg-[var(--color-primary-dark)]",
    outline: "border border-[var(--color-border)] text-[var(--color-text)] hover:bg-gray-50",
    ghost: "text-[var(--color-primary)] hover:bg-[var(--color-primary-light)]",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      className={`${baseStyles} ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
}

export default Button;
