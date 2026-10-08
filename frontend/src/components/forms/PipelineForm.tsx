import { useState } from 'react';
import ApiResultPanel from '../ApiResultPanel';
import FormField from '../FormField';
import TestFormCard, { buttonClass } from '../TestFormCard';
import { callApi, type ApiResult } from '../../services/api';

function PipelineForm() {
  const [pipeline, setPipeline] = useState('bogus');
  const [result, setResult] = useState<ApiResult | null>(null);

  const run = async () => {
    setResult(await callApi('post', `/mlops/run-pipeline?pipeline=${encodeURIComponent(pipeline)}`));
  };

  return (
    <TestFormCard
      title="MLOps pipeline runner"
      testCases="TC-16"
      hint="Valid names: all, patient, trial, sales, doctor. An unknown name such as “bogus” must return 404 (the old code reported it as completed)."
    >
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <div className="w-60"><FormField label="Pipeline name" type="text" value={pipeline} onChange={setPipeline} /></div>
          <button className={buttonClass} onClick={run}>Run pipeline</button>
        </div>
        <ApiResultPanel result={result} />
      </div>
    </TestFormCard>
  );
}

export default PipelineForm;
