import { Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import PipelineForm from '../components/forms/PipelineForm';
import AnomalyPanel from '../components/AnomalyPanel';
import ChartCard from '../components/ChartCard';
import DataState, { SourceNote } from '../components/DataState';
import MetricCard from '../components/MetricCard';
import useApiData from '../hooks/useApiData';
import type { MonitoringStatus, NameValue, Overview, Recommendation, SalesForecast } from '../types/analytics';
import { formatMoney, formatNumber } from '../utils/formatters';

type ExecutiveOverview = {
  kpis: Overview;
  revenue_forecast: SalesForecast;
  risk_distribution: NameValue[];
};

const RISK_COLORS: Record<string, string> = { HIGH: '#ea580c', LOW: '#2563eb' };

function ExecutiveDashboard() {
  const executive = useApiData<ExecutiveOverview>('/executive/overview');
  const recommendations = useApiData<{ recommendations: Recommendation[] }>('/analytics/recommendations');
  const monitoring = useApiData<MonitoringStatus>('/model-monitoring/status');
  const k = executive.data?.kpis;

  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Executive Insights</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">PharmaIQ Executive Dashboard</h1>
      </header>

      <DataState loading={executive.loading} error={executive.error} ready={!!k}>
        {k && executive.data && (
          <>
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
              <MetricCard title="Total Patients" value={formatNumber(k.total_patients)} subtitle={`${formatNumber(k.high_risk_patients)} high risk`} />
              <MetricCard title="Active Trial Participants" value={formatNumber(k.active_trial_participants)} subtitle={`Dropout ${k.trial_dropout_rate}%`} />
              <MetricCard title="High-Value Doctors" value={formatNumber(k.high_value_doctors)} subtitle={`of ${formatNumber(k.total_doctors)}`} />
              <MetricCard title="Revenue Forecast (3 months)" value={formatMoney(k.revenue_forecast_3m)} subtitle={`Total to date ${formatMoney(k.total_revenue)}`} />
            </div>
            <SourceNote files="patients.csv · clinical_trials.csv · pharma_sales.csv · doctors.csv" updated={k.last_updated} />

            <div className="grid gap-5 xl:grid-cols-3">
              <ChartCard title="Revenue Forecast by Month">
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={executive.data.revenue_forecast.forecast}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis tickFormatter={formatMoney} width={70} />
                    <Tooltip formatter={(value: number) => formatMoney(value)} />
                    <Bar dataKey="revenue" name="Forecast revenue" fill="#2563eb" />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>
              <ChartCard title="Patient Risk Distribution">
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie isAnimationActive={false} data={executive.data.risk_distribution} dataKey="value" nameKey="name" outerRadius={95} label={({ name, value }) => `${name}: ${value}`}>
                      {executive.data.risk_distribution.map((entry) => <Cell key={entry.name} fill={RISK_COLORS[entry.name] ?? '#64748b'} />)}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>
              <ChartCard title="Data-Driven Recommendations">
                <ul className="space-y-3 text-sm text-slate-700">
                  {recommendations.data?.recommendations.map((item) => (
                    <li key={item.text}>
                      <span className="mr-2 rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-700">{item.area}</span>
                      {item.text}
                    </li>
                  ))}
                </ul>
              </ChartCard>
            </div>
          </>
        )}
      </DataState>

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Model Monitoring</h2>
        {monitoring.error && <p className="mt-3 text-sm text-rose-700">{monitoring.error}</p>}
        {monitoring.data && (
          <>
            <div className="mt-4 overflow-x-auto rounded-2xl border border-slate-200">
              <table className="min-w-full text-left text-sm">
                <thead className="bg-slate-100 text-slate-700">
                  <tr>{['Model', 'Metric', 'Value', 'Status', 'Trained'].map((label) => <th key={label} className="px-3 py-2 font-semibold">{label}</th>)}</tr>
                </thead>
                <tbody>
                  {monitoring.data.models.map((model) => (
                    <tr key={model.name} className="border-t border-slate-200">
                      <td className="px-3 py-2 font-medium">{model.name}</td>
                      <td className="px-3 py-2">{model.metric}</td>
                      <td className="px-3 py-2">{model.accuracy}</td>
                      <td className="px-3 py-2">{model.status}</td>
                      <td className="px-3 py-2">{model.trained_at ? new Date(model.trained_at).toLocaleString() : '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="mt-3 text-sm text-slate-600">
              Data drift on {monitoring.data.data_drift.feature} ({monitoring.data.data_drift.dataset}): PSI {monitoring.data.data_drift.psi}, status{' '}
              <b>{monitoring.data.data_drift.status}</b>. Method: {monitoring.data.data_drift.method}.
            </p>
          </>
        )}
      </section>

      <AnomalyPanel kind="patient" title="Patients with unusual clinical profiles" />
      <PipelineForm />
    </div>
  );
}

export default ExecutiveDashboard;
