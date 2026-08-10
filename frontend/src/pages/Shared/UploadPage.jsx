import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";
import { getAdvisors, getCustomers, uploadAudio } from "../../services/fitnovaService";

function UploadPage() {
  const [advisors, setAdvisors] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [advisorId, setAdvisorId] = useState("");
  const [customerId, setCustomerId] = useState("");
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => { Promise.all([getAdvisors(), getCustomers()]).then(([advisorData, customerData]) => { setAdvisors(advisorData); setCustomers(customerData); }).catch(() => setError("Unable to load upload options.")); }, []);
  async function submit(event) {
    event.preventDefault();
    if (!file || !advisorId || !customerId) { setError("Select an advisor, customer, and audio file."); return; }
    setError(""); setLoading(true);
    try { const result = await uploadAudio({ advisorId, customerId, file }); setMessage(`Upload complete. Call #${result.call_id} is ready for processing.`); }
    catch (requestError) { setError(requestError.response?.data?.detail || "Upload failed."); }
    finally { setLoading(false); }
  }
  return (
    <DashboardLayout>
      <h1 className="text-xl font-semibold text-[var(--color-text)] mb-6">Upload call recording</h1>
      <Card>
        <form onSubmit={submit} className="space-y-4 max-w-xl">
          <div>
            <label className="block text-sm font-medium text-[var(--color-text)] mb-1">Select Advisor</label>
            <select
              value={advisorId}
              onChange={(event) => setAdvisorId(event.target.value)}
              className="w-full p-2 border border-[var(--color-border)] rounded-lg text-sm bg-white"
            >
              <option value="">Select advisor</option>
              {advisors.map((advisor) => (
                <option key={advisor.id} value={advisor.id}>
                  {advisor.first_name} {advisor.last_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-[var(--color-text)] mb-1">Select Customer</label>
            <select
              value={customerId}
              onChange={(event) => setCustomerId(event.target.value)}
              className="w-full p-2 border border-[var(--color-border)] rounded-lg text-sm bg-white"
            >
              <option value="">Select customer</option>
              {customers.map((customer) => (
                <option key={customer.id} value={customer.id}>
                  {customer.first_name} {customer.last_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-[var(--color-text)] mb-1">Audio File</label>
            <input
              type="file"
              accept="audio/wav,audio/mpeg,audio/mp4,.wav,.mp3,.m4a,.mpeg"
              onChange={(event) => setFile(event.target.files?.[0] || null)}
              className="w-full px-3 py-2 border border-[var(--color-border)] rounded-lg text-sm bg-white cursor-pointer file:mr-4 file:py-1 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-[var(--color-primary-light)] file:text-[var(--color-primary)] hover:file:bg-[var(--color-primary)] hover:file:text-white"
            />
          </div>

          {error && <p className="text-sm text-red-600">{error}</p>}
          {message && <p className="text-sm text-green-600">{message}</p>}

          <Button type="submit" disabled={loading}>
            {loading ? "Uploading…" : "Upload audio"}
          </Button>
        </form>
      </Card>
    </DashboardLayout>
  );
}

export default UploadPage;
