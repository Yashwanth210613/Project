export default function ReportCard({ report }) {
  const alerts = report.decision_support?.abnormal_labs || [];

  return (
    <div className="border rounded p-4 bg-white space-y-3">
      <h3 className="font-bold">{report.original_filename}</h3>
      <div>
        <p className="font-semibold">Structured Data</p>
        <ul className="text-sm list-disc ml-5">
          {(report.structured_data || []).map((item, idx) => (
            <li key={idx}>
              {item.labName ? `${item.labName}: ${item.labValue}` : `${item.medicine} ${item.dosage} ${item.frequency}`}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <p className="font-semibold">Alerts</p>
        {alerts.length === 0 ? <p className="text-green-600">No abnormalities</p> : alerts.map((a, i) => <p key={i} className="text-red-600">{a}</p>)}
      </div>
      <p className="text-sm bg-blue-50 p-2 rounded">{report.explanation}</p>
    </div>
  );
}
