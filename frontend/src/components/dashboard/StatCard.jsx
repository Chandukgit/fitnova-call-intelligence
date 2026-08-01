import { motion } from "framer-motion";
import Card from "../common/Card";

// Displays one KPI number with an icon and label.
// icon: a lucide-react icon component passed in as a prop
function StatCard({ label, value, icon: Icon, suffix = "" }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="flex items-center justify-between">
        <div>
          <p className="text-xs text-[var(--color-text-soft)] mb-1">{label}</p>
          <p className="text-2xl font-semibold text-[var(--color-text)]">
            {value}
            {suffix}
          </p>
        </div>
        {Icon && (
          <div className="p-3 rounded-lg bg-[var(--color-primary-light)]">
            <Icon size={20} className="text-[var(--color-primary)]" />
          </div>
        )}
      </Card>
    </motion.div>
  );
}

export default StatCard;
