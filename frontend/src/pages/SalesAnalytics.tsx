import { Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import SalesForecastForm from '../components/forms/SalesForecastForm';
import AnomalyPanel from '../components/AnomalyPanel';
import ChartCard from '../components/ChartCard';
import DataState, { SourceNote } from '../components/DataState';
import MetricCard from '../components/MetricCard';
import useApiData from '../hooks/useApiData';
import type { SalesAnalytics as SalesStats } from '../types/analytics';
import { formatMoney, formatNumber } from '../utils/formatters';

const MEDICINE_COLORS = ['#2563eb', '#ea580c', '#0ea5e9'];

function SalesAnalytics() {
  const { data: s, loading, error } = useApiData<SalesStats>('/analytics/sales');

  const trend = s
    ? [
        ...s.monthly.filter((row) => row.complete).map((row) => ({ month: row.month, actual: row.revenue })),
        ...s.forecast.forecast.map((row) => ({ month: row.month, forecast: row.revenue }))
      ]
    : [];

  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Commercial Intelligence</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Sales Forecasting & Analytics</h1>
      </header>

      <SalesForecastForm />

      <DataState loading={loading} error={error} ready={!!s}>
        {s && (
          <>
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
              <MetricCard title="Total Revenue" value={formatMoney(s.total_revenue)} subtitle={`${s.period.start} to ${s.period.end}`} />
              <MetricCard title="Units Sold" value={formatNumber(s.total_units)} subtitle="All medicines and regions" />
              <MetricCard title="Marketing ROI" value={`${s.roi.toFixed(2)}x`} subtitle={`${formatMoney(s.total_marketing)} spent`} />
              <MetricCard title="Next 3 Months (forecast)" value={formatMoney(s.forecast.next_3_months_revenue)} subtitle={`Recent growth ${s.recent_growth_pct}%`} />
            </div>
            <SourceNote files="pharma_sales.csv" />

            <ChartCard title="Monthly Revenue and 3-Month Forecast">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" minTickGap={30} />
                  <YAxis tickFormatter={formatMoney} width={70} />
                  <Tooltip formatter={(value: number) => formatMoney(value)} />
                  <Legend />
                  <Line type="monotone" dataKey="actual" name="Actual" stroke="#2563eb" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="forecast" name="Forecast" stroke="#ea580c" strokeWidth={3} strokeDasharray="6 4" />
                </LineChart>
              </ResponsiveContainer>
              <p className="mt-2 text-xs text-slate-500">{s.forecast.method}; the latest partial month is excluded.</p>
            </ChartCard>

            <div className="grid gap-5 xl:grid-cols-3">
              <ChartCard title="Revenue by Region">
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={s.by_region}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="region" />
                    <YAxis tickFormatter={formatMoney} width={70} />
                    <Tooltip formatter={(value: number) => formatMoney(value)} />
                    <Bar dataKey="revenue" name="Revenue" fill="#2563eb" />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>
              <ChartCard title="Revenue Share by Medicine">
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie isAnimationActive={false} data={s.by_medicine} dataKey="revenue" nameKey="medicine" outerRadius={95} label={({ medicine, share_pct }) => `${medicine}: ${share_pct}%`}>
                      {s.by_medicine.map((entry, index) => <Cell key={entry.medicine} fill={MEDICINE_COLORS[index % MEDICINE_COLORS.length]} />)}
                    </Pie>
                    <Tooltip formatter={(value: number) => formatMoney(value)} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>
              <ChartCard title="Marketing ROI by Medicine (revenue per $)">
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={s.by_medicine}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="medicine" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="roi" name="ROI" fill="#ea580c" />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>
          </>
        )}
      </DataState>

      <AnomalyPanel kind="sales" title="Unusual sales days (|z| ≥ 3)" />
    </div>
  );
}

export default SalesAnalytics;
