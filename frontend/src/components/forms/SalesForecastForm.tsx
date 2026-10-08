import { useState } from 'react';
import ApiResultPanel from '../ApiResultPanel';
import FormField, { numericPayload } from '../FormField';
import TestFormCard, { buttonClass } from '../TestFormCard';
import { callApi, type ApiResult } from '../../services/api';

function SalesForecastForm() {
  const [values, setValues] = useState<Record<string, string>>({ sales_units: '100', marketing_spend: '1000' });
  const [result, setResult] = useState<ApiResult | null>(null);

  const run = async () => {
    setResult(await callApi('post', '/forecast/sales', numericPayload(values, ['sales_units', 'marketing_spend'])));
  };

  return (
    <TestFormCard
      title="Stock forecast"
      testCases="TC-09"
      hint="100 units should recommend 110 in stock (the old code said 15,000). Boundary: spend 25000 gives +10%, 25001 gives +18%. Negative units must be rejected."
    >
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <div className="grid gap-3 sm:grid-cols-2">
            <FormField label="Units sold" value={values.sales_units} onChange={(value) => setValues({ ...values, sales_units: value })} />
            <FormField label="Marketing spend" value={values.marketing_spend} onChange={(value) => setValues({ ...values, marketing_spend: value })} />
          </div>
          <button className={buttonClass} onClick={run}>Forecast</button>
        </div>
        <ApiResultPanel result={result} />
      </div>
    </TestFormCard>
  );
}

export default SalesForecastForm;
