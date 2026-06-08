import { useEffect, useState } from 'react';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';
import api from '../services/api';

function ExecutiveDashboard() {
  const [kpis, setKpis] = useState<any>(null);

  useEffect(() => {
    api.get('/dashboard/kpis')
      .then((response) => setKpis(response.data))
      .catch(() => setKpis(null));
  }, []);

  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Executive Insights</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">PharmaIQ Executive Dashboard</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard title="Total Patients" value={kpis ? `${kpis.total_patients}` : '...'} />
        <MetricCard title="Active Trials" value={kpis ? `${kpis.active_trials}` : '...'} />
        <MetricCard title="High Risk Patients" value={kpis ? `${kpis.high_risk_patients}` : '...'} />
        <MetricCard title="Revenue Forecast" value={kpis ? `$${kpis.revenue_forecast}M` : '...'} />
      </div>

      <div className="grid gap-5 xl:grid-cols-3">
        <ChartCard title="Revenue Forecast Trend">
          <div className="flex h-full items-center justify-center text-slate-500">Forecast visualization placeholder</div>
        </ChartCard>
        <ChartCard title="Risk Distribution">
          <div className="flex h-full items-center justify-center text-slate-500">Risk distribution placeholder</div>
        </ChartCard>
        <ChartCard title="Recommendations">
          <div className="space-y-3 text-slate-700">
            <p>• Expand high-value physician engagement.</p>
            <p>• Accelerate adherence programs for medium-risk patients.</p>
            <p>• Optimize pharma inventory for high-demand regions.</p>
          </div>
        </ChartCard>
      </div>
    </div>
  );
}

export default ExecutiveDashboard;
