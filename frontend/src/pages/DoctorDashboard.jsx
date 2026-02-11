import { useState } from 'react';
import api from '../services/api';
import ReportCard from '../components/ReportCard';

export default function DoctorDashboard() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);

  const upload = async () => {
    if (!file) return;
    const fd = new FormData();
    fd.append('file', file);
    const { data } = await api.post('/reports/upload', fd);
    setReport({ original_filename: file.name, ...data });
  };

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-2xl font-bold">Doctor Dashboard</h1>
      <div className="bg-white rounded shadow p-4 space-y-3">
        <p>Upload handwritten prescription image or lab PDF.</p>
        <input type="file" onChange={(e) => setFile(e.target.files?.[0])} />
        <button onClick={upload} className="bg-blue-600 text-white px-4 py-2 rounded">Process Report</button>
      </div>
      {report && <ReportCard report={report} />}
    </div>
  );
}
