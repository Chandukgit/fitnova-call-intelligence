import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import Card from "../../components/common/Card";
import RecentCallsTable from "../../components/dashboard/RecentCallsTable";
import LoadingSkeleton from "../../components/common/LoadingSkeleton";
import { getCalls } from "../../services/mockService";

// A simple reports page. For now it just reuses the calls table,
// since real reporting will depend on the backend later.
function ReportsPage() {
  const [calls, setCalls] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCalls().then((data) => {
      setCalls(data);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <LoadingSkeleton className="h-64 w-full" />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">Reports</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">
        Call summary report (mock data - full reporting comes with the backend).
      </p>

      <Card title="All Calls">
        <RecentCallsTable calls={calls} />
      </Card>
    </DashboardLayout>
  );
}

export default ReportsPage;
