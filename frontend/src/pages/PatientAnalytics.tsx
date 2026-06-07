import DataTable from '../components/DataTable';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';

const patients = [
  { patient_id: 1001, name: 'Anna Patel', age: 52, gender: 'Female', disease: 'Diabetes', risk_score: 87 },
  { patient_id: 1002, name: 'Marcus Lee', age: 38, gender: 'Male', disease: 'Hypertension', risk_score: 63 },
  { patient_id: 1003, name: 'Sana Khan', age: 67, gender: 'Female', disease: 'Cardiovascular', risk_score: 74 }
];

function PatientAnalytics() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Patient Analytics</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Risk Prediction Summary</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        <MetricCard title="Average Risk" value="68%" subtitle="Across active population" />
        <MetricCard title="High Risk Patients" value="110" subtitle="Requires follow-up" />
        <MetricCard title="Low Risk Patients" value="520" subtitle="Stable treatment" />
      </div>

      <div className="grid gap-5 lg:grid-cols-3">
        <ChartCard title="Risk Category Distribution">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for pie or chart</div>
        </ChartCard>
        <ChartCard title="Disease Mix">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for stacked bars</div>
        </ChartCard>
        <ChartCard title="Model Health">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for evaluation metrics</div>
        </ChartCard>
      </div>

      <div>
        <h2 className="mb-4 text-xl font-semibold text-slate-900">Patient Risk Table</h2>
        <DataTable
          columns={[
            { key: 'patient_id', label: 'ID' },
            { key: 'name', label: 'Name' },
            { key: 'age', label: 'Age' },
            { key: 'gender', label: 'Gender' },
            { key: 'disease', label: 'Disease' },
            { key: 'risk_score', label: 'Risk (%)' }
          ]}
          data={patients}
        />
      </div>
    </div>
  );
}

export default PatientAnalytics;
