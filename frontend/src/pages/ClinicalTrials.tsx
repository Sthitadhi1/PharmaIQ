import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter } from 'recharts';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';

const dropoutData = [
  { month: 'Month 1', completion: 98, dropout_risk: 2 },
  { month: 'Month 3', completion: 94, dropout_risk: 6 },
  { month: 'Month 6', completion: 88, dropout_risk: 12 },
  { month: 'Month 9', completion: 81, dropout_risk: 19 },
  { month: 'Month 12', completion: 72, dropout_risk: 28 }
];

const sitePerformance = [
  { site: 'Site A', enrollment: 85, completion: 78 },
  { site: 'Site B', enrollment: 72, completion: 65 },
  { site: 'Site C', enrollment: 91, completion: 88 },
  { site: 'Site D', enrollment: 68, completion: 55 }
];

const phaseData = [
  { phase: 'Phase I', trials: 12, success_rate: 95 },
  { phase: 'Phase II', trials: 8, success_rate: 85 },
  { phase: 'Phase III', trials: 5, success_rate: 72 },
  { phase: 'Phase IV', trials: 3, success_rate: 88 }
];

function ClinicalTrials() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Clinical Operations</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Trial Dropout Intelligence</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        <MetricCard title="Overall Completion" value="81%" subtitle="Trial portfolio" />
        <MetricCard title="Dropout Risk (Avg)" value="18%" subtitle="At-risk patients" />
        <MetricCard title="High-Risk Alerts" value="14" subtitle="Intervention needed" />
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Dropout Trend Over Time">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={dropoutData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="completion" stroke="#10b981" strokeWidth={2} name="Completion %" />
              <Line type="monotone" dataKey="dropout_risk" stroke="#ef4444" strokeWidth={2} name="Dropout Risk %" />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Site Performance Comparison">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={sitePerformance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="site" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="enrollment" fill="#3b82f6" name="Enrolled" />
              <Bar dataKey="completion" fill="#10b981" name="Completed" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Trial Phase Success Rates">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={phaseData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="phase" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="trials" fill="#8b5cf6" name="Active Trials" />
              <Bar dataKey="success_rate" fill="#10b981" name="Success Rate %" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Risk Assessment Summary">
          <div className="space-y-4 p-4">
            <div className="flex items-center justify-between rounded-lg bg-red-50 p-3">
              <span className="text-sm font-semibold text-slate-700">High Risk</span>
              <span className="text-lg font-bold text-red-600">14 patients</span>
            </div>
            <div className="flex items-center justify-between rounded-lg bg-yellow-50 p-3">
              <span className="text-sm font-semibold text-slate-700">Medium Risk</span>
              <span className="text-lg font-bold text-yellow-600">32 patients</span>
            </div>
            <div className="flex items-center justify-between rounded-lg bg-green-50 p-3">
              <span className="text-sm font-semibold text-slate-700">Low Risk</span>
              <span className="text-lg font-bold text-green-600">154 patients</span>
            </div>
          </div>
        </ChartCard>
      </div>
    </div>
  );
}

export default ClinicalTrials;
