import { useState } from 'react';
import ApiResultPanel from '../ApiResultPanel';
import FormField, { numericPayload } from '../FormField';
import TestFormCard, { buttonClass, secondaryButtonClass } from '../TestFormCard';
import { callApi, type ApiResult } from '../../services/api';

const RULE_FIELDS: [string, string][] = [
  ['age', 'Age (years)'],
  ['glucose_level', 'Glucose (mg/dL)'],
  ['previous_visits', 'Previous visits']
];
const ML_FIELDS: [string, string][] = [
  ['treatment_duration', 'Treatment duration (days)'],
  ['blood_pressure_systolic', 'Systolic BP'],
  ['blood_pressure_diastolic', 'Diastolic BP']
];
const DEFAULTS = {
  age: '72',
  glucose_level: '190',
  previous_visits: '9',
  treatment_duration: '12',
  blood_pressure_systolic: '160',
  blood_pressure_diastolic: '100'
};

function PatientRiskForm() {
  const [values, setValues] = useState<Record<string, string>>(DEFAULTS);
  const [result, setResult] = useState<ApiResult | null>(null);
  const [busy, setBusy] = useState(false);

  const run = async (url: string, keys: string[]) => {
    setBusy(true);
    setResult(await callApi('post', url, numericPayload(values, keys)));
    setBusy(false);
  };
  const ruleKeys = RULE_FIELDS.map(([key]) => key);
  const allKeys = [...ruleKeys, ...ML_FIELDS.map(([key]) => key)];

  return (
    <TestFormCard
      title="Patient risk calculator"
      testCases="TC-05 · TC-06 · TC-07 · TC-12"
      hint={
        <>
          Defaults give 84.3 HIGH (TC-05). Try age −1, 0, 120 and 121 (TC-06), or clear a field (TC-07).
          "ML model" uses all six fields (TC-12).
        </>
      }
    >
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <div className="grid gap-3 sm:grid-cols-3">
            {RULE_FIELDS.map(([key, label]) => (
              <FormField key={key} label={label} value={values[key]} onChange={(value) => setValues({ ...values, [key]: value })} />
            ))}
          </div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">ML model only</p>
          <div className="grid gap-3 sm:grid-cols-3">
            {ML_FIELDS.map(([key, label]) => (
              <FormField key={key} label={label} value={values[key]} onChange={(value) => setValues({ ...values, [key]: value })} />
            ))}
          </div>
          <div className="flex flex-wrap gap-3">
            <button className={buttonClass} disabled={busy} onClick={() => run('/predict/patient-risk', ruleKeys)}>
              Predict (rule-based)
            </button>
            <button className={secondaryButtonClass} disabled={busy} onClick={() => run('/ml/patient-risk', allKeys)}>
              Predict (ML model)
            </button>
            <button className={secondaryButtonClass} disabled={busy} onClick={() => setValues(DEFAULTS)}>
              Reset values
            </button>
          </div>
        </div>
        <ApiResultPanel result={result} />
      </div>
    </TestFormCard>
  );
}

export default PatientRiskForm;
