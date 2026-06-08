import { PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';
import DataTable from '../components/DataTable';

const riskData = [
  { name: 'Low Risk', value: 520, fill: '#10b981' },
  { name: 'Medium Risk', value: 320, fill: '#f59e0b' },
  { name: 'High Risk', value: 110, fill: '#ef4444' }
];

const riskTrendData = [
  { month: 'Jan', avg_risk: 55 },
  { month: 'Feb', avg_risk: 58 },
  { month: 'Mar', avg_risk: 62 },
  { month: 'Apr', avg_risk: 65 },
  { month: 'May', avg_risk: 68 },
  { month: 'Jun', avg_risk: 70 }
];

const diseaseData = [
  { disease: 'Diabetes', count: 240 },
  { disease: 'Hypertension', count: 185 },
  { disease: 'Cardiac', count: 160 },
  { disease: 'Respiratory', count: 120 }
];

const patients = [
  { patient_id: 1001, name: 'Anna Patel', age: 52, gender: 'Female', disease: 'Diabetes', risk_score: 87 },
  { patient_id: 1002, name: 'Marcus Lee', age: 38, gender: 'Male', disease: 'Hypertension', risk_score: 63 },
  { patient_id: 1003, name: 'Sana Khan', age: 67, gender: 'Female', disease: 'Cardiovascular', risk_score: 74 }
];

function PatientAnalytics() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Patient Intelligence</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Risk Prediction Analytics</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        <MetricCard title="Average Risk Score" value="68%" subtitle="Population health metric" />
        <MetricCard title="High Risk Patients" value="110" subtitle="Requires intervention" />
        <MetricCard title="Total Monitored" value="950" subtitle="Active patient cohort" />
      </div>

      <div className="grid gap-5 xl:grid-cols-3">
        <ChartCard title="Risk Category Distribution">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={riskData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {riskData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Disease Distribution">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart
              layout="vertical"
              data={diseaseData}
              margin={{ top: 5, right: 30, left: 200, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="disease" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Model Performance">
          <div className="space-y-3 p-4">
            <div>
              <p className="text-sm font-semibold text-slate-700">Accuracy</p>
              <div className="mt-1 h-2 rounded-full bg-slate-200">
                <div className="h-full w-4/5 rounded-full bg-green-500"></div>
              </div>
              <p className="mt-1 text-sm text-slate-600">85%</p>
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-700">Precision</p>
              <div className="mt-1 h-2 rounded-full bg-slate-200">
                <div className="h-full w-3/4 rounded-full bg-blue-500"></div>
              </div>
              <p className="mt-1 text-sm text-slate-600">82%</p>
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-700">Recall</p>
              <div className="mt-1 h-2 rounded-full bg-slate-200">
                <div className="h-full w-4/5 rounded-full bg-purple-500"></div>
              </div>
              <p className="mt-1 text-sm text-slate-600">88%</p>
            </div>
          </div>
        </ChartCard>
      </div>

      <ChartCard title="Average Risk Score Trend">
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={riskTrendData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="avg_risk" stroke="#ef4444" strokeWidth={3} name="Avg Risk Score" />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>

      <div>
        <h2 className="mb-4 text-xl font-semibold text-slate-900">Patient Risk Details</h2>
        <DataTable
          columns={[
            { key: 'patient_id', label: 'ID' },
            { key: 'name', label: 'Patient Name' },
            { key: 'age', label: 'Age' },
            { key: 'gender', label: 'Gender' },
            { key: 'disease', label: 'Condition' },
            { key: 'risk_score', label: 'Risk Score (%)' }
          ]}
          data={patients}
        />
      </div>
    </div>
  );
}

export default PatientAnalytics;
