import { Link } from "react-router-dom";
import Button from "../../components/common/Button";

// Simple 404 page for unmatched routes.
function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-5xl font-bold text-[var(--color-primary)] mb-2">404</h1>
      <p className="text-[var(--color-text)] font-medium mb-1">Page not found</p>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">
        The page you're looking for doesn't exist.
      </p>
      <Link to="/">
        <Button>Back to Login</Button>
      </Link>
    </div>
  );
}

export default NotFoundPage;
