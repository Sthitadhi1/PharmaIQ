import { useState } from 'react';
import ApiResultPanel from '../ApiResultPanel';
import FormField from '../FormField';
import TestFormCard, { buttonClass } from '../TestFormCard';
import { callApi, type ApiResult } from '../../services/api';

function PatientListPanel() {
  const [limit, setLimit] = useState('5');
  const [offset, setOffset] = useState('0');
  const [result, setResult] = useState<ApiResult | null>(null);

  const load = async () => {
    const query = new URLSearchParams({ limit, offset }).toString();
    setResult(await callApi('get', `/patients?${query}`));
  };

  const rows: Record<string, unknown>[] = result?.ok ? result.data.patients : [];
  const columns = rows.length ? Object.keys(rows[0]) : [];

  return (
    <TestFormCard
      title="Patient records from the dataset"
      testCases="TC-11"
      hint="Loads real rows from patients.csv. Valid limit is 1–500; try limit 0 or 501, or offset −1."
    >
      <div className="flex flex-wrap items-end gap-3">
        <div className="w-32"><FormField label="Limit" value={limit} onChange={setLimit} /></div>
        <div className="w-32"><FormField label="Offset" value={offset} onChange={setOffset} /></div>
        <button className={buttonClass} onClick={load}>Load patients</button>
      </div>
      <div className="mt-5 space-y-4">
        {result && !result.ok && <ApiResultPanel result={result} />}
        {result?.ok && (
          <>
            <p className="text-sm text-slate-600">
              <span className="rounded-full border border-emerald-300 bg-emerald-100 px-3 py-1 font-semibold text-emerald-800">HTTP {result.status}</span>
              <span className="ml-3">Showing {rows.length} of {result.data.total} patients (offset {result.data.offset})</span>
            </p>
            <div className="overflow-x-auto rounded-2xl border border-slate-200">
              <table className="min-w-full text-left text-sm">
                <thead className="bg-slate-100 text-slate-700">
                  <tr>{columns.map((column) => <th key={column} className="px-3 py-2 font-semibold">{column}</th>)}</tr>
                </thead>
                <tbody>
                  {rows.map((row, index) => (
                    <tr key={index} className="border-t border-slate-200">
                      {columns.map((column) => <td key={column} className="px-3 py-2 text-slate-800">{String(row[column])}</td>)}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </TestFormCard>
  );
}

export default PatientListPanel;
