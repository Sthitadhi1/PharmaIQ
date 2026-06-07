import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, CartesianGrid } from 'recharts';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';

const overviewMetrics = [
  { title: 'Total Patients', value: '1,920' },
  { title: 'Active Trials', value: '28' },
  { title: 'High Risk Patients', value: '314' },
  { title: 'Revenue Forecast', value: '$4.8M' }
];

const trendData = [
  { month: 'Jan', value: 420 },
  { month: 'Feb', value: 540 },
  { month: 'Mar', value: 610 },
  { month: 'Apr', value: 720 },
  { month: 'May', value: 650 },
  { month: 'Jun', value: 780 }
];

const regionData = [
  { region: 'North', sales: 320 },
  { region: 'South', sales: 270 },
  { region: 'East', sales: 200 },
  { region: 'West', sales: 170 }
];

function DashboardHome() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Executive Dashboard</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">PharmaIQ Overview</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        {overviewMetrics.map((metric) => (
          <MetricCard key={metric.title} title={metric.title} value={metric.value} />
        ))}
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Monthly Revenue Trend">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#2563eb" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Regional Sales Performance">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={regionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="sales" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
}

export default DashboardHome;
