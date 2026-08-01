import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import Card from "../../components/common/Card";
import RecentCallsTable from "../../components/dashboard/RecentCallsTable";
import LoadingSkeleton from "../../components/common/LoadingSkeleton";
import { getCalls } from "../../services/mockService";

// Lists every call so the user can click into any of them.
function CallsListPage() {
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
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">Calls</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">Every recorded call, analyzed by AI.</p>

      <Card title="All Calls">
        <RecentCallsTable calls={calls} />
      </Card>
    </DashboardLayout>
  );
}

export default CallsListPage;
