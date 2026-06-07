import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, CartesianGrid } from 'recharts';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';

const metrics = [
  { title: 'Total Patients', value: '1,920' },
  { title: 'Active Trials', value: '28' },
  { title: 'High Risk Patients', value: '314' },
  { title: 'Revenue Forecast', value: '$4.8M' }
];

const riskData = [
  { name: 'Low', value: 30 },
  { name: 'Medium', value: 45 },
  { name: 'High', value: 25 }
];

const salesData = [
  { month: 'Jan', revenue: 420 },
  { month: 'Feb', revenue: 540 },
  { month: 'Mar', revenue: 610 },
  { month: 'Apr', revenue: 720 },
  { month: 'May', revenue: 650 },
  { month: 'Jun', revenue: 780 }
];

function Dashboard() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Enterprise Analytics</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">PharmaIQ Dashboard</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        {metrics.map((metric) => (
          <MetricCard key={metric.title} title={metric.title} value={metric.value} />
        ))}
      </div>

      <div className="grid gap-5 xl:grid-cols-3">
        <ChartCard title="Patient Risk Distribution">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder chart</div>
        </ChartCard>
        <ChartCard title="Clinical Trial Performance">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder chart</div>
        </ChartCard>
        <ChartCard title="Doctor Segments">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder chart</div>
        </ChartCard>
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Sales Trends">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={salesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="revenue" stroke="#2563eb" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
        <ChartCard title="Revenue Forecast">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={salesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="revenue" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
}

export default Dashboard;
