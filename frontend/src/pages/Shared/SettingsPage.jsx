import DashboardLayout from "../../components/layout/DashboardLayout";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

// Basic settings page. No real save logic yet - just UI.
function SettingsPage() {
  return (
    <DashboardLayout>
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-1">Settings</h1>
      <p className="text-sm text-[var(--color-text-soft)] mb-6">Manage your account preferences.</p>

      <Card title="Profile" className="max-w-lg">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-[var(--color-text)] mb-1">Full Name</label>
            <input
              type="text"
              defaultValue="Sarah Director"
              className="w-full px-3 py-2 border border-[var(--color-border)] rounded-lg text-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-[var(--color-text)] mb-1">Email</label>
            <input
              type="email"
              defaultValue="sarah@fitnova.com"
              className="w-full px-3 py-2 border border-[var(--color-border)] rounded-lg text-sm"
            />
          </div>

          <Button>Save Changes</Button>
        </div>
      </Card>
    </DashboardLayout>
  );
}

export default SettingsPage;
