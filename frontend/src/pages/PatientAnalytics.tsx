import { Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import PatientRiskForm from '../components/forms/PatientRiskForm';
import PatientListPanel from '../components/forms/PatientListPanel';
import ExplainPatientForm from '../components/forms/ExplainPatientForm';
import ChartCard from '../components/ChartCard';
import DataState, { SourceNote } from '../components/DataState';
import MetricCard from '../components/MetricCard';
import useApiData from '../hooks/useApiData';
import type { PatientAnalytics as PatientStats } from '../types/analytics';

const RISK_COLORS: Record<string, string> = { HIGH: '#ea580c', LOW: '#2563eb' };

type ModelMetrics = Record<string, Record<string, number | string>>;

function PatientAnalytics() {
  const stats = useApiData<PatientStats>('/analytics/patients');
  const metrics = useApiData<ModelMetrics>('/analytics/model-metrics');
  const s = stats.data;
  const model = metrics.data?.patient_risk;

  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Patient Intelligence</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Risk Prediction Analytics</h1>
      </header>

      <PatientRiskForm />

      <DataState loading={stats.loading} error={stats.error} ready={!!s}>
        {s && (
          <>
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
              <MetricCard title="Patients Monitored" value={String(s.total_patients)} subtitle={`Average age ${s.avg_age}`} />
              <MetricCard title="High-Risk Patients" value={String(s.high_risk_patients)} subtitle={`${s.high_risk_pct}% of all patients`} />
              <MetricCard title="Avg Medication Adherence" value={`${s.avg_adherence}%`} subtitle="Across all patients" />
              <MetricCard title="Diabetic Patients" value={`${s.diabetic_pct}%`} subtitle="Share of the cohort" />
            </div>
            <SourceNote files="patients.csv" />

            <div className="grid gap-5 xl:grid-cols-3">
              <ChartCard title="Risk Level Distribution">
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie isAnimationActive={false} data={s.risk_distribution} dataKey="value" nameKey="name" outerRadius={95} label={({ name, value }) => `${name}: ${value}`}>
                      {s.risk_distribution.map((entry) => <Cell key={entry.name} fill={RISK_COLORS[entry.name] ?? '#64748b'} />)}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>

              <ChartCard title="High-Risk Share by Age Group (%)">
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={s.by_age_group}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="age_group" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Bar dataKey="high_risk_pct" name="High risk %" fill="#ea580c" />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>

              <ChartCard title="Risk Model Performance (test set)">
                {model ? (
                  <div className="space-y-4 p-2">
                    {(['accuracy', 'precision', 'recall', 'f1_score'] as const).map((key) => {
                      const value = Number(model[key] ?? 0) * 100;
                      return (
                        <div key={key}>
                          <div className="flex justify-between text-sm">
                            <span className="font-semibold capitalize text-slate-700">{key.replace('_', ' ')}</span>
                            <span className="text-slate-600">{value.toFixed(1)}%</span>
                          </div>
                          <div className="mt-1 h-2 rounded-full bg-slate-200">
                            <div className="h-full rounded-full bg-blue-600" style={{ width: `${value}%` }} />
                          </div>
                        </div>
                      );
                    })}
                    <p className="text-xs text-slate-500">Trained {String(model.trained_at ?? '')} on {String(model.samples ?? '')} samples</p>
                  </div>
                ) : (
                  <p className="text-sm text-slate-500">Model not trained yet. Run python -m ml_engine.training.train_all.</p>
                )}
              </ChartCard>
            </div>

            <ChartCard title="High-Risk vs Low-Risk Patients: Averages">
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={s.by_risk_level}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="risk_level" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="avg_adherence" name="Adherence %" fill="#2563eb" />
                  <Bar dataKey="avg_admissions" name="Prior admissions" fill="#ea580c" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
          </>
        )}
      </DataState>

      <ExplainPatientForm />
      <PatientListPanel />
    </div>
  );
}

export default PatientAnalytics;
