import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import DoctorSegmentForm from '../components/forms/DoctorSegmentForm';
import ChartCard from '../components/ChartCard';
import DataState, { SourceNote } from '../components/DataState';
import MetricCard from '../components/MetricCard';
import useApiData from '../hooks/useApiData';
import type { DoctorAnalytics } from '../types/analytics';
import { formatMoney, formatNumber } from '../utils/formatters';

function DoctorSegmentation() {
  const { data: d, loading, error } = useApiData<DoctorAnalytics>('/analytics/doctors');

  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">HCP Intelligence</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Doctor Segmentation</h1>
      </header>

      <DoctorSegmentForm />

      <DataState loading={loading} error={error} ready={!!d}>
        {d && (
          <>
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
              <MetricCard title="Doctors" value={formatNumber(d.total_doctors)} subtitle="In the HCP dataset" />
              <MetricCard title="Average Engagement" value={String(d.avg_engagement)} subtitle="Score out of 100" />
              <MetricCard title="High-Value Doctors" value={formatNumber(d.high_value_doctors)} subtitle="Segment A (engagement ≥ 80)" />
              <MetricCard title="Sales Generated" value={formatMoney(d.total_sales_generated)} subtitle="All doctors" />
            </div>
            <SourceNote files="doctors.csv" />

            <div className="grid gap-5 xl:grid-cols-3">
              <ChartCard title="Doctors per Segment">
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={[...d.segments].sort((a, b) => a.segment.localeCompare(b.segment))}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="segment" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="doctors" name="Doctors" fill="#2563eb" />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>
              <ChartCard title="Engagement by Specialization">
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={d.by_specialization}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="specialization" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Bar dataKey="avg_engagement" name="Avg engagement" fill="#ea580c" />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>
              <ChartCard title="Sales and Engagement by Region">
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={d.by_region}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="region" />
                    <YAxis yAxisId="sales" tickFormatter={formatMoney} width={70} />
                    <YAxis yAxisId="engagement" orientation="right" domain={[0, 100]} />
                    <Tooltip />
                    <Legend />
                    <Bar yAxisId="sales" dataKey="sales" name="Sales generated" fill="#2563eb" />
                    <Bar yAxisId="engagement" dataKey="avg_engagement" name="Avg engagement" fill="#ea580c" />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>

            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-slate-900">Top 10 Doctors by Sales Generated</h2>
              <div className="mt-4 overflow-x-auto rounded-2xl border border-slate-200">
                <table className="min-w-full text-left text-sm">
                  <thead className="bg-slate-100 text-slate-700">
                    <tr>
                      {['Doctor ID', 'Specialization', 'Region', 'Engagement', 'Sales generated', 'Segment'].map((label) => (
                        <th key={label} className="px-3 py-2 font-semibold">{label}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {d.top_doctors.map((doctor) => (
                      <tr key={doctor.doctor_id} className="border-t border-slate-200">
                        <td className="px-3 py-2">{doctor.doctor_id}</td>
                        <td className="px-3 py-2">{doctor.specialization}</td>
                        <td className="px-3 py-2">{doctor.region}</td>
                        <td className="px-3 py-2">{doctor.engagement_score}</td>
                        <td className="px-3 py-2">{formatMoney(doctor.sales_generated)}</td>
                        <td className="px-3 py-2">{doctor.segment}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}
      </DataState>
    </div>
  );
}

export default DoctorSegmentation;
