import { useState } from "react";
import { motion } from "framer-motion";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import Footer from "./Footer";

// This is the shared layout used by every dashboard page.
// It wraps the page content ("children") with Navbar + Sidebar + Footer.
function DashboardLayout({ children, role }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <div className="h-screen flex flex-col">
      <Navbar onToggleSidebar={() => setIsSidebarOpen((open) => !open)} role={role} />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar isOpen={isSidebarOpen} />

        <main className="flex-1 overflow-y-auto bg-gray-50">
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
            className="p-4 md:p-6"
          >
            {children}
          </motion.div>
        </main>
      </div>

      <Footer />
    </div>
  );
}

export default DashboardLayout;
