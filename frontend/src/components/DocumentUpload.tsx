import type { ChangeEvent } from 'react';

type DocumentUploadProps = {
  onUpload: (file: File) => void;
};

function DocumentUpload({ onUpload }: DocumentUploadProps) {
  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-900">Upload Document</h2>
      <p className="mt-2 text-slate-600">Accepts PDF, TXT, and CSV files for RAG-based analysis.</p>
      <label className="mt-4 flex cursor-pointer items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-slate-50 px-4 py-6 text-center text-slate-600 transition hover:border-slate-400">
        <input type="file" accept=".pdf,.txt,.csv" onChange={handleFileChange} className="hidden" />
        <span>Choose a document to upload</span>
      </label>
    </div>
  );
}

export default DocumentUpload;
