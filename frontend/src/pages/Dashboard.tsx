import { Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import ChartCard from '../components/ChartCard';
import DataState, { SourceNote } from '../components/DataState';
import MetricCard from '../components/MetricCard';
import useApiData from '../hooks/useApiData';
import type { DoctorAnalytics, Overview, PatientAnalytics, SalesAnalytics, TrialAnalytics } from '../types/analytics';
import { formatMoney, formatNumber } from '../utils/formatters';

const RISK_COLORS: Record<string, string> = { HIGH: '#ea580c', LOW: '#2563eb' };
const SEGMENT_COLORS = ['#2563eb', '#0ea5e9', '#94a3b8'];

function Dashboard() {
  const overview = useApiData<Overview>('/analytics/overview');
  const patients = useApiData<PatientAnalytics>('/analytics/patients');
  const trials = useApiData<TrialAnalytics>('/analytics/trials');
  const sales = useApiData<SalesAnalytics>('/analytics/sales');
  const doctors = useApiData<DoctorAnalytics>('/analytics/doctors');
  const all = [overview, patients, trials, sales, doctors];
  const reload = () => all.forEach((item) => item.reload());

  const o = overview.data;
  const revenueChart = sales.data
    ? [
        ...sales.data.monthly.filter((row) => row.complete).slice(-9).map((row) => ({ month: row.month, actual: row.revenue })),
        ...sales.data.forecast.forecast.map((row) => ({ month: row.month, forecast: row.revenue }))
      ]
    : [];

  return (
    <div className="space-y-8">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Enterprise Analytics</p>
          <h1 className="mt-3 text-3xl font-semibold text-slate-900">PharmaIQ Dashboard</h1>
        </div>
        <button onClick={reload} className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold hover:bg-slate-100">
          Refresh data
        </button>
      </header>

      <DataState loading={all.some((item) => item.loading)} error={all.find((item) => item.error)?.error ?? null} ready={!!o}>
        {o && (
          <>
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
              <MetricCard title="Total Patients" value={formatNumber(o.total_patients)} subtitle={`${formatNumber(o.high_risk_patients)} high risk (${o.high_risk_pct}%)`} />
              <MetricCard title="Active Trial Participants" value={formatNumber(o.active_trial_participants)} subtitle={`of ${formatNumber(o.trial_participants)}; dropout ${o.trial_dropout_rate}%`} />
              <MetricCard title="Total Revenue" value={formatMoney(o.total_revenue)} subtitle={`Last 3 months ${o.recent_growth_pct >= 0 ? '+' : ''}${o.recent_growth_pct}% vs prior 3`} />
              <MetricCard title="Revenue Forecast (3 months)" value={formatMoney(o.revenue_forecast_3m)} subtitle="Linear trend on monthly revenue" />
            </div>
            <SourceNote files="patients.csv · clinical_trials.csv · pharma_sales.csv · doctors.csv" updated={o.last_updated} />
          </>
        )}

        <div className="grid gap-5 xl:grid-cols-3">
          <ChartCard title="Patient Risk Distribution">
            {patients.data && (
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie isAnimationActive={false} data={patients.data.risk_distribution} dataKey="value" nameKey="name" outerRadius={95} label={({ name, value }) => `${name}: ${value}`}>
                    {patients.data.risk_distribution.map((entry) => <Cell key={entry.name} fill={RISK_COLORS[entry.name] ?? '#64748b'} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            )}
          </ChartCard>
          <ChartCard title="Trial Dropout Rate by Phase (%)">
            {trials.data && (
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={trials.data.by_phase}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="phase" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Bar dataKey="dropout_rate" name="Dropout %" fill="#ea580c" />
                </BarChart>
              </ResponsiveContainer>
            )}
          </ChartCard>
          <ChartCard title="Doctor Segments">
            {doctors.data && (
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie isAnimationActive={false} data={doctors.data.segments} dataKey="doctors" nameKey="segment" outerRadius={95} label={({ segment, doctors: count }) => `${segment}: ${count}`}>
                    {doctors.data.segments.map((entry, index) => <Cell key={entry.segment} fill={SEGMENT_COLORS[index % SEGMENT_COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            )}
          </ChartCard>
        </div>

        <div className="grid gap-5 xl:grid-cols-2">
          <ChartCard title="Monthly Revenue">
            {sales.data && (
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={sales.data.monthly}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" minTickGap={30} />
                  <YAxis tickFormatter={formatMoney} width={70} />
                  <Tooltip formatter={(value: number) => formatMoney(value)} />
                  <Line type="monotone" dataKey="revenue" stroke="#2563eb" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            )}
          </ChartCard>
          <ChartCard title="Revenue: Recent Months and 3-Month Forecast">
            {sales.data && (
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={revenueChart}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis tickFormatter={formatMoney} width={70} />
                  <Tooltip formatter={(value: number) => formatMoney(value)} />
                  <Legend />
                  <Bar dataKey="actual" name="Actual" fill="#2563eb" />
                  <Bar dataKey="forecast" name="Forecast" fill="#ea580c" />
                </BarChart>
              </ResponsiveContainer>
            )}
          </ChartCard>
        </div>
      </DataState>
    </div>
  );
}

export default Dashboard;
