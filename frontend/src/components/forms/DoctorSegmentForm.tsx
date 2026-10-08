import { useState } from 'react';
import ApiResultPanel from '../ApiResultPanel';
import FormField, { numericPayload } from '../FormField';
import TestFormCard, { buttonClass } from '../TestFormCard';
import { callApi, type ApiResult } from '../../services/api';

function DoctorSegmentForm() {
  const [score, setScore] = useState('79.9');
  const [result, setResult] = useState<ApiResult | null>(null);

  const run = async () => {
    setResult(await callApi('post', '/segment/doctors', numericPayload({ engagement_score: score }, ['engagement_score'])));
  };

  return (
    <TestFormCard
      title="Doctor segment calculator"
      testCases="TC-10"
      hint="Boundary values: 80 → Segment A, 79.9 → B, 60 → B, 59.9 → C. Scores outside 0–100 must be rejected."
    >
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <div className="w-60"><FormField label="Engagement score (0–100)" value={score} onChange={setScore} /></div>
          <div className="flex flex-wrap gap-2">
            {['80', '79.9', '60', '59.9'].map((value) => (
              <button key={value} className="rounded-full border border-slate-300 px-3 py-1 text-sm hover:bg-slate-100" onClick={() => setScore(value)}>
                {value}
              </button>
            ))}
          </div>
          <button className={buttonClass} onClick={run}>Find segment</button>
        </div>
        <ApiResultPanel result={result} />
      </div>
    </TestFormCard>
  );
}

export default DoctorSegmentForm;
