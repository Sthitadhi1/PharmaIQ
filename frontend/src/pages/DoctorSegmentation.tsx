import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';

function DoctorSegmentation() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Doctor Segmentation</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Provider Engagement Analytics</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        <MetricCard title="High Value Doctors" value="72" subtitle="Segment A" />
        <MetricCard title="Growth Opportunities" value="45" subtitle="Segment B" />
        <MetricCard title="Low Engagement" value="26" subtitle="Segment C" />
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Engagement Clusters">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for clustering visualization</div>
        </ChartCard>
        <ChartCard title="Prescription Trends">
          <div className="flex h-full items-center justify-center text-slate-500">Placeholder for prescription analytics</div>
        </ChartCard>
      </div>
    </div>
  );
}

export default DoctorSegmentation;
