import { Search, Bell, Menu } from "lucide-react";
import Badge from "../common/Badge";

// Top navigation bar shown on every dashboard page.
// onToggleSidebar lets the navbar collapse/expand the sidebar.
function Navbar({ onToggleSidebar, role = "Sales Director" }) {
  return (
    <header className="h-16 bg-white border-b border-[var(--color-border)] flex items-center justify-between px-4 md:px-6">
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg hover:bg-gray-100 lg:hidden"
          aria-label="Toggle sidebar"
        >
          <Menu size={20} />
        </button>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-[var(--color-primary)] flex items-center justify-center text-white font-bold text-sm">
            F
          </div>
          <span className="font-semibold text-[var(--color-text)] hidden sm:block">FitNova</span>
        </div>
      </div>

      <div className="hidden md:flex items-center flex-1 max-w-md mx-6">
        <div className="relative w-full">
          <Search
            size={16}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-soft)]"
          />
          <input
            type="text"
            placeholder="Search calls, advisors..."
            className="w-full pl-9 pr-3 py-2 text-sm border border-[var(--color-border)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/30"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="relative p-2 rounded-lg hover:bg-gray-100" aria-label="Notifications">
          <Bell size={18} className="text-[var(--color-text)]" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-[var(--color-primary)] rounded-full" />
        </button>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-xs font-semibold text-[var(--color-text)]">
            SD
          </div>
          <div className="hidden md:block">
            <p className="text-sm font-medium leading-tight">Sarah Director</p>
            <Badge colorClass="bg-[var(--color-primary-light)] text-[var(--color-primary)]">{role}</Badge>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
