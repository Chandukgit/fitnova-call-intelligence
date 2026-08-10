import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Dumbbell } from "lucide-react";
import Button from "../../components/common/Button";
import { login } from "../../services/fitnovaService";

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user = await login(email, password, rememberMe);
      navigate({ ADMIN: "/director", MANAGER: "/leader", ADVISOR: "/advisor" }[user.role] || "/calls");
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Unable to sign in. Check your credentials and try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* Left side - Login form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="w-full max-w-sm"
        >
          <div className="flex items-center gap-2 mb-8">
            <div className="w-9 h-9 rounded-lg bg-[var(--color-primary)] flex items-center justify-center text-white font-bold">
              F
            </div>
            <span className="text-lg font-semibold">FitNova</span>
          </div>

          <h1 className="text-2xl font-semibold text-[var(--color-text)] mb-1">Welcome back</h1>
          <p className="text-sm text-[var(--color-text-soft)] mb-6">
            Sign in to view your call intelligence dashboard.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-[var(--color-text)] mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@fitnova.com"
                className="w-full px-3 py-2 border border-[var(--color-border)] rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/30"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-[var(--color-text)] mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3 py-2 border border-[var(--color-border)] rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/30"
              />
            </div>

            {error && <p className="text-sm text-red-600" role="alert">{error}</p>}

            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 text-[var(--color-text-soft)]">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded border-[var(--color-border)]"
                />
                Remember me
              </label>
              <a href="#" className="text-[var(--color-primary)] font-medium">
                Forgot password?
              </a>
            </div>

            <Button type="submit" className="w-full">
              {loading ? "Signing in…" : "Login"}
            </Button>
          </form>
        </motion.div>
      </div>

      {/* Right side - Illustration placeholder */}
      <div className="hidden lg:flex w-1/2 bg-[var(--color-primary-light)] items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          className="text-center px-10"
        >
          <div className="w-40 h-40 mx-auto rounded-full bg-white flex items-center justify-center mb-6 shadow-sm">
            <Dumbbell size={56} className="text-[var(--color-primary)]" />
          </div>
          <h2 className="text-xl font-semibold text-[var(--color-text)] mb-2">
            AI insight for every sales call
          </h2>
          <p className="text-sm text-[var(--color-text-soft)] max-w-xs mx-auto">
            FitNova helps fitness sales teams understand what happens on every call, and coach smarter.
          </p>
        </motion.div>
      </div>
    </div>
  );
}

export default LoginPage;
