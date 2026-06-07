import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';

function SalesAnalytics() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Sales Intelligence</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Commercial Forecasting</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        <MetricCard title="Forecast Accuracy" value="89%" />
        <MetricCard title="Demand Growth" value="+12%" />
        <MetricCard title="Stock Recommendation" value="25,000 units" />
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Regional Demand">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for demand analytics</div>
        </ChartCard>
        <ChartCard title="Revenue by Medicine">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for medicine forecast</div>
        </ChartCard>
      </div>
    </div>
  );
}

export default SalesAnalytics;
