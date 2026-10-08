import type { ApiResult } from '../services/api';

const STATUS_TEXT: Record<number, string> = {
  0: 'No response',
  200: 'OK',
  400: 'Bad request',
  401: 'Unauthorized',
  404: 'Not found',
  413: 'File too large',
  415: 'Unsupported file type',
  422: 'Validation error',
  429: 'Too many requests',
  500: 'Server error',
  503: 'Service unavailable'
};

const badgeClass = (status: number) => {
  if (status >= 200 && status < 300) return 'bg-emerald-100 text-emerald-800 border-emerald-300';
  if (status >= 400 && status < 500) return 'bg-amber-100 text-amber-800 border-amber-300';
  return 'bg-rose-100 text-rose-800 border-rose-300';
};

const formatValue = (value: unknown) => {
  if (value === null || value === undefined) return '—';
  const text = typeof value === 'object' ? JSON.stringify(value) : String(value);
  return text.length > 60 ? `${text.slice(0, 60)}…` : text;
};

// Keeps passwords off the screen when the raw request is expanded during a demo.
const maskSecrets = (body: unknown) =>
  body && typeof body === 'object' && 'password' in body ? { ...body, password: '••••••••' } : body;

function ResponseBody({ data }: { data: any }) {
  const detail = data?.detail;
  if (Array.isArray(detail)) {
    return (
      <ul className="space-y-1 text-sm text-amber-900">
        {detail.map((item, index) => (
          <li key={index}>
            <span className="font-mono font-semibold">{(item.loc ?? []).slice(1).join('.') || 'request'}</span>: {item.msg}
          </li>
        ))}
      </ul>
    );
  }
  if (typeof detail === 'string') {
    return <p className="text-sm text-slate-800">{detail}</p>;
  }
  if (data && typeof data === 'object' && !Array.isArray(data)) {
    return (
      <dl className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-1 text-sm">
        {Object.entries(data).map(([key, value]) => (
          <div key={key} className="contents">
            <dt className="font-mono text-slate-500">{key}</dt>
            <dd className="font-medium text-slate-900 break-all">{formatValue(value)}</dd>
          </div>
        ))}
      </dl>
    );
  }
  return <p className="text-sm text-slate-800">{formatValue(data)}</p>;
}

function ApiResultPanel({ result }: { result: ApiResult | null }) {
  if (!result) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-300 p-4 text-sm text-slate-500">
        Run a request to see the server's status code and response here.
      </div>
    );
  }

  return (
    <div className="space-y-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <div className="flex flex-wrap items-center gap-3">
        <span className={`rounded-full border px-3 py-1 text-sm font-semibold ${badgeClass(result.status)}`}>
          HTTP {result.status} · {STATUS_TEXT[result.status] ?? ''}
        </span>
        <span className="font-mono text-xs text-slate-500">
          {result.request.method} {result.request.url}
        </span>
      </div>
      <ResponseBody data={result.data} />
      <details className="text-xs text-slate-600">
        <summary className="cursor-pointer select-none">Raw request and response</summary>
        <pre className="mt-2 overflow-x-auto rounded-xl bg-slate-900 p-3 text-slate-100">
{`Request body:\n${JSON.stringify(maskSecrets(result.request.body) ?? null, null, 2)}\n\nResponse body:\n${JSON.stringify(result.data, null, 2)}`}
        </pre>
      </details>
    </div>
  );
}

export default ApiResultPanel;
