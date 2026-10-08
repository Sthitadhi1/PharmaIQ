import { useState } from 'react';
import ApiResultPanel from '../ApiResultPanel';
import FormField from '../FormField';
import TestFormCard, { buttonClass } from '../TestFormCard';
import { callApi, type ApiResult } from '../../services/api';

type Factor = { feature: string; impact: string; value: number; dataset_average: number };

function ExplainPatientForm() {
  const [patientId, setPatientId] = useState('1');
  const [result, setResult] = useState<ApiResult | null>(null);

  const run = async () => {
    setResult(await callApi('get', `/explainability/patient/${encodeURIComponent(patientId.trim())}`));
  };

  const details = result?.ok ? result.data : null;
  const factors: Factor[] = details?.details?.top_risk_factors ?? [];

  return (
    <TestFormCard
      title="Why is this patient high or low risk?"
      testCases="Explainability"
      hint="Fits a logistic regression on patients.csv and shows which features pushed this patient's risk up or down. Valid IDs: 0–999."
    >
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <div className="w-48"><FormField label="Patient ID" value={patientId} onChange={setPatientId} /></div>
          <button className={buttonClass} onClick={run}>Explain prediction</button>
          {details && (
            <div className="space-y-3 rounded-2xl border border-slate-200 p-4">
              <p className="text-lg font-semibold text-slate-900">
                {details.prediction} · {details.details.risk_score}% probability
              </p>
              <p className="text-sm text-slate-600">Recorded risk level in the dataset: {details.details.recorded_risk_level}</p>
              {factors.map((factor) => (
                <div key={factor.feature}>
                  <div className="flex justify-between text-sm">
                    <span className="font-medium text-slate-800">{factor.feature}: {factor.value} (avg {factor.dataset_average})</span>
                    <span className="text-slate-600">{factor.impact}</span>
                  </div>
                  <div className="mt-1 h-2 rounded-full bg-slate-200">
                    <div className="h-full rounded-full bg-orange-500" style={{ width: factor.impact }} />
                  </div>
                </div>
              ))}
              <p className="text-sm text-slate-700">{details.reason}</p>
            </div>
          )}
        </div>
        <ApiResultPanel result={result} />
      </div>
    </TestFormCard>
  );
}

export default ExplainPatientForm;
