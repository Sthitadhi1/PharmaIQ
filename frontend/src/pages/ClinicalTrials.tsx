import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import TrialDropoutForm from '../components/forms/TrialDropoutForm';
import AnomalyPanel from '../components/AnomalyPanel';
import ChartCard from '../components/ChartCard';
import DataState, { SourceNote } from '../components/DataState';
import MetricCard from '../components/MetricCard';
import useApiData from '../hooks/useApiData';
import type { TrialAnalytics } from '../types/analytics';
import { formatNumber } from '../utils/formatters';

function RateChart({ title, data, dataKey }: { title: string; data: object[]; dataKey: string }) {
  return (
    <ChartCard title={title}>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={dataKey} />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="completion_rate" name="Completion %" stackId="a" fill="#2563eb" />
          <Bar dataKey="dropout_rate" name="Dropout %" stackId="a" fill="#ea580c" />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function ClinicalTrials() {
  const { data: t, loading, error } = useApiData<TrialAnalytics>('/analytics/trials');

  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Clinical Operations</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Clinical Trial Analytics</h1>
      </header>

      <TrialDropoutForm />

      <DataState loading={loading} error={error} ready={!!t}>
        {t && (
          <>
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
              <MetricCard title="Participants" value={formatNumber(t.participants)} subtitle={`${formatNumber(t.active_participants)} still enrolled`} />
              <MetricCard title="Completion Rate" value={`${t.completion_rate}%`} subtitle="Across all phases" />
              <MetricCard title="Dropout Rate" value={`${t.dropout_rate}%`} subtitle={`${formatNumber(t.dropouts)} participants left`} />
              <MetricCard title="High Side Effects" value={formatNumber(t.high_side_effect_participants)} subtitle={`Avg duration ${Math.round(t.avg_duration_days)} days`} />
            </div>
            <SourceNote files="clinical_trials.csv" />

            <div className="grid gap-5 xl:grid-cols-2">
              <RateChart title="Completion vs Dropout by Phase (%)" data={t.by_phase} dataKey="phase" />
              <RateChart title="Completion vs Dropout by Side-Effect Severity (%)" data={t.by_side_effects} dataKey="side_effects" />
              <RateChart title="Completion vs Dropout by Trial Duration (%)" data={t.by_duration} dataKey="duration_group" />
              <RateChart title="Completion vs Dropout by Age Group (%)" data={t.by_age_group} dataKey="age_group" />
            </div>
          </>
        )}
      </DataState>

      <AnomalyPanel kind="trial" title="Trial groups with unusual dropout (z-test)" />
    </div>
  );
}

export default ClinicalTrials;
