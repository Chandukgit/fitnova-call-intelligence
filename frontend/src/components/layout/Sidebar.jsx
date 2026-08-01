import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";
import { LayoutDashboard, PhoneCall, BarChart2, FileText, Settings } from "lucide-react";

// Sidebar menu items. Each has an icon, a label, and a route.
const menuItems = [
  { label: "Dashboard", icon: LayoutDashboard, path: "/director" },
  { label: "Calls", icon: PhoneCall, path: "/calls" },
  { label: "Analytics", icon: BarChart2, path: "/analytics" },
  { label: "Reports", icon: FileText, path: "/reports" },
  { label: "Settings", icon: Settings, path: "/settings" },
];

// isOpen controls whether the sidebar is expanded or collapsed to icons only.
function Sidebar({ isOpen }) {
  return (
    <motion.aside
      animate={{ width: isOpen ? 220 : 72 }}
      transition={{ duration: 0.2 }}
      className="h-full bg-[var(--color-sidebar)] border-r border-[var(--color-border)] overflow-hidden hidden lg:block"
    >
      <nav className="py-4">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-5 py-3 text-sm font-medium transition-colors ${
                isActive
                  ? "text-[var(--color-primary)] bg-[var(--color-primary-light)] border-r-2 border-[var(--color-primary)]"
                  : "text-[var(--color-text-soft)] hover:bg-gray-50"
              }`
            }
          >
            <item.icon size={18} />
            {isOpen && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>
    </motion.aside>
  );
}

export default Sidebar;
