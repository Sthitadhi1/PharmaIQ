import type { ReactNode } from 'react';

type TestFormCardProps = {
  title: string;
  testCases: string;
  hint: ReactNode;
  children: ReactNode;
};

function TestFormCard({ title, testCases, hint, children }: TestFormCardProps) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-baseline justify-between gap-3">
        <h2 className="text-xl font-semibold text-slate-900">{title}</h2>
        <span className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold tracking-wide text-white">{testCases}</span>
      </div>
      <p className="mt-2 text-sm text-slate-600">{hint}</p>
      <div className="mt-5">{children}</div>
    </section>
  );
}

export default TestFormCard;

export const buttonClass =
  'rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:opacity-50';
export const secondaryButtonClass =
  'rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-800 transition hover:bg-slate-100 disabled:opacity-50';
