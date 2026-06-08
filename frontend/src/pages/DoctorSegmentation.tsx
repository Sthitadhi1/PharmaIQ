import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';
import DataTable from '../components/DataTable';

const segmentDistribution = [
  { name: 'High Value', value: 72, fill: '#10b981' },
  { name: 'Growth Opportunity', value: 45, fill: '#f59e0b' },
  { name: 'Low Engagement', value: 26, fill: '#ef4444' }
];

const engagementMetrics = [
  { segment: 'High Value', prescriptions: 980, patients: 245, engagement: 89.2 },
  { segment: 'Growth Opp', prescriptions: 740, patients: 180, engagement: 72.5 },
  { segment: 'Low Engagement', prescriptions: 320, patients: 85, engagement: 42.3 }
];

const regionDistribution = [
  { region: 'North', high_value: 20, growth: 12, low: 8 },
  { region: 'South', high_value: 18, growth: 15, low: 10 },
  { region: 'East', high_value: 22, growth: 10, low: 5 },
  { region: 'West', high_value: 12, growth: 8, low: 3 }
];

const doctorData = [
  { doctor_id: 4001, name: 'Dr. Meera Joshi', specialization: 'Cardiology', engagement_score: 89.2, segment: 'High Value' },
  { doctor_id: 4002, name: 'Dr. Ravi Singh', specialization: 'Endocrinology', engagement_score: 72.5, segment: 'Growth Opp' },
  { doctor_id: 4003, name: 'Dr. Priya Sharma', specialization: 'Neurology', engagement_score: 42.3, segment: 'Low Engagement' }
];

function DoctorSegmentation() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Provider Analytics</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Healthcare Provider Segmentation</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        <MetricCard title="High Value Doctors" value="72" subtitle="Top engagement tier" />
        <MetricCard title="Growth Opportunities" value="45" subtitle="Development focus" />
        <MetricCard title="Low Engagement" value="26" subtitle="Reactivation needed" />
      </div>

      <div className="grid gap-5 xl:grid-cols-3">
        <ChartCard title="Doctor Segment Distribution">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={segmentDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {segmentDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Segment Performance Metrics">
          <div className="space-y-3 p-4">
            <div className="rounded-lg bg-green-50 p-3">
              <p className="text-xs font-semibold uppercase text-slate-600">High Value Segment</p>
              <p className="mt-1 text-lg font-bold text-green-600">89.2 avg engagement</p>
              <p className="text-xs text-slate-500">980 total prescriptions</p>
            </div>
            <div className="rounded-lg bg-yellow-50 p-3">
              <p className="text-xs font-semibold uppercase text-slate-600">Growth Opportunity</p>
              <p className="mt-1 text-lg font-bold text-yellow-600">72.5 avg engagement</p>
              <p className="text-xs text-slate-500">740 total prescriptions</p>
            </div>
            <div className="rounded-lg bg-red-50 p-3">
              <p className="text-xs font-semibold uppercase text-slate-600">Low Engagement</p>
              <p className="mt-1 text-lg font-bold text-red-600">42.3 avg engagement</p>
              <p className="text-xs text-slate-500">320 total prescriptions</p>
            </div>
          </div>
        </ChartCard>

        <ChartCard title="Regional Distribution">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={regionDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="high_value" fill="#10b981" name="High Value" />
              <Bar dataKey="growth" fill="#f59e0b" name="Growth" />
              <Bar dataKey="low" fill="#ef4444" name="Low Engagement" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div>
        <h2 className="mb-4 text-xl font-semibold text-slate-900">Doctor Engagement Rankings</h2>
        <DataTable
          columns={[
            { key: 'doctor_id', label: 'ID' },
            { key: 'name', label: 'Doctor Name' },
            { key: 'specialization', label: 'Specialization' },
            { key: 'engagement_score', label: 'Engagement Score' },
            { key: 'segment', label: 'Segment' }
          ]}
          data={doctorData}
        />
      </div>
    </div>
  );
}

export default DoctorSegmentation;
