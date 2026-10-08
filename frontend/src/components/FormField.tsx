type FormFieldProps = {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: 'number' | 'text' | 'password';
};

// No min/max on purpose: invalid values must reach the server so its validation can be demonstrated.
function FormField({ label, value, onChange, type = 'number' }: FormFieldProps) {
  return (
    <label className="block">
      <span className="text-sm font-medium text-slate-700">{label}</span>
      <input
        type={type}
        step={type === 'number' ? 'any' : undefined}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 outline-none focus:border-slate-500"
      />
    </label>
  );
}

export default FormField;

// Builds a JSON body from form values; empty fields are left out so "missing field" cases can be tested.
export const numericPayload = (values: Record<string, string>, keys: string[]) =>
  Object.fromEntries(keys.filter((key) => values[key].trim() !== '').map((key) => [key, Number(values[key])]));
