import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';

function SalesIntelligence() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Sales Intelligence</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Forecasting & Performance</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        <MetricCard title="Month-over-month" value="+12%" subtitle="Forecast growth" />
        <MetricCard title="Demand Accuracy" value="89%" subtitle="Model confidence" />
        <MetricCard title="Stock Recommendation" value="25,000" subtitle="Units suggested" />
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Medicine Sales Trend">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for sales line chart</div>
        </ChartCard>
        <ChartCard title="Regional Forecasts">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for region analysis</div>
        </ChartCard>
      </div>
    </div>
  );
}

export default SalesIntelligence;
