import { useEffect, useState } from 'react';
import api from '../services/api';
import ReportCard from '../components/ReportCard';

export default function PatientDashboard() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    const load = async () => {
      const { data } = await api.get('/reports/');
      const detailed = await Promise.all(data.map((r) => api.get(`/reports/${r.id}`).then((res) => res.data)));
      setReports(detailed);
    };
    load();
  }, []);

  return (
    <div className="p-8 space-y-5">
      <h1 className="text-2xl font-bold">Patient Dashboard</h1>
      <p className="text-gray-600">Your explained reports and health summary.</p>
      {reports.map((r) => <ReportCard key={r.id} report={r} />)}
      {reports.length === 0 && <p>No reports available yet.</p>}
    </div>
  );
}
