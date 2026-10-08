import type { ReactNode } from 'react';

type DataStateProps = {
  loading: boolean;
  error: string | null;
  ready: boolean;
  children: ReactNode;
};

// Shows a loading or error panel until the live data has arrived.
function DataState({ loading, error, ready, children }: DataStateProps) {
  if (error) {
    return <div className="rounded-3xl border border-rose-200 bg-rose-50 p-6 text-sm text-rose-800">{error}</div>;
  }
  if (loading && !ready) {
    return <div className="rounded-3xl border border-slate-200 bg-white p-6 text-sm text-slate-500">Loading live data…</div>;
  }
  return <>{children}</>;
}

export default DataState;

export function SourceNote({ files, updated }: { files: string; updated?: string }) {
  return (
    <p className="text-xs text-slate-500">
      Live from <span className="font-mono">{files}</span>
      {updated ? ` · data last modified ${new Date(updated).toLocaleString()}` : ''}
    </p>
  );
}
