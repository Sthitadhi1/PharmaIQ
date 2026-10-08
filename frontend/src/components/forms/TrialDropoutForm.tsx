import { useState } from 'react';
import ApiResultPanel from '../ApiResultPanel';
import FormField, { numericPayload } from '../FormField';
import TestFormCard, { buttonClass } from '../TestFormCard';
import { callApi, type ApiResult } from '../../services/api';

function TrialDropoutForm() {
  const [values, setValues] = useState<Record<string, string>>({ completion_rate: '40', previous_missed_visits: '3' });
  const [sideEffects, setSideEffects] = useState('HIGH');
  const [result, setResult] = useState<ApiResult | null>(null);

  const run = async () => {
    const body = { ...numericPayload(values, ['completion_rate', 'previous_missed_visits']), side_effects: sideEffects };
    setResult(await callApi('post', '/predict/trial-dropout', body));
  };

  return (
    <TestFormCard
      title="Trial dropout predictor"
      testCases="TC-08"
      hint="Defaults give 64% HIGH with reason “Multiple missed visits”. Try completion rate 140 (must be rejected), or 0 missed visits with HIGH side effects to see the reason change."
    >
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <div className="grid gap-3 sm:grid-cols-3">
            <FormField label="Completion rate (%)" value={values.completion_rate} onChange={(value) => setValues({ ...values, completion_rate: value })} />
            <FormField label="Missed visits" value={values.previous_missed_visits} onChange={(value) => setValues({ ...values, previous_missed_visits: value })} />
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Side effects</span>
              <select
                value={sideEffects}
                onChange={(event) => setSideEffects(event.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900"
              >
                {['NONE', 'LOW', 'MEDIUM', 'HIGH'].map((level) => <option key={level}>{level}</option>)}
              </select>
            </label>
          </div>
          <button className={buttonClass} onClick={run}>Predict dropout</button>
        </div>
        <ApiResultPanel result={result} />
      </div>
    </TestFormCard>
  );
}

export default TrialDropoutForm;
