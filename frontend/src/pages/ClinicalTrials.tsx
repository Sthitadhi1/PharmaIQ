import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';

function ClinicalTrials() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Clinical Trial Intelligence</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Dropout Prediction Insights</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        <MetricCard title="Completion Rate" value="81%" subtitle="Trial portfolio health" />
        <MetricCard title="Dropout Risk" value="18%" subtitle="At-risk patients" />
        <MetricCard title="Engagement Alerts" value="14" subtitle="Needs follow-up" />
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Dropout Probability Trends">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for probability trend</div>
        </ChartCard>
        <ChartCard title="Site Performance Overview">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for site charts</div>
        </ChartCard>
      </div>
    </div>
  );
}

export default ClinicalTrials;
