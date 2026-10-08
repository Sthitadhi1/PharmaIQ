import useApiData from '../hooks/useApiData';
import type { AnomalyResult } from '../types/analytics';

function AnomalyPanel({ kind, title }: { kind: 'sales' | 'patient' | 'trial'; title: string }) {
  const { data, error } = useApiData<AnomalyResult>(`/anomalies/${kind}`);
  const columns = data?.items.length ? Object.keys(data.items[0]) : [];

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-baseline justify-between gap-3">
        <h2 className="text-xl font-semibold text-slate-900">{title}</h2>
        {data && (
          <span className={`rounded-full px-3 py-1 text-xs font-semibold ${data.anomaly ? 'bg-orange-100 text-orange-800' : 'bg-blue-100 text-blue-800'}`}>
            {data.anomaly ? `${data.count} found` : 'None found'}
          </span>
        )}
      </div>
      {error && <p className="mt-3 text-sm text-rose-700">{error}</p>}
      {data && (
        <>
          <p className="mt-2 text-sm text-slate-600">
            {data.message} Checked {data.records_checked.toLocaleString()} records · method: {data.method}.
          </p>
          {data.items.length > 0 && (
            <div className="mt-4 overflow-x-auto rounded-2xl border border-slate-200">
              <table className="min-w-full text-left text-sm">
                <thead className="bg-slate-100 text-slate-700">
                  <tr>{columns.map((column) => <th key={column} className="px-3 py-2 font-semibold">{column}</th>)}</tr>
                </thead>
                <tbody>
                  {data.items.map((item, index) => (
                    <tr key={index} className="border-t border-slate-200">
                      {columns.map((column) => <td key={column} className="px-3 py-2">{String(item[column])}</td>)}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </section>
  );
}

export default AnomalyPanel;
