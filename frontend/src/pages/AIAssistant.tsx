import { useState } from 'react';
import ChatInterface from '../components/ChatInterface';
import DocumentUpload from '../components/DocumentUpload';
import useApiData from '../hooks/useApiData';
import { getErrorMessage, queryAiAssistant, uploadAiDocument } from '../services/api';

type LlmStatus = { provider: string; model: string; state: string; last_error: string | null };

type AiStatus = {
  status: string;
  datasets: Array<{ name: string; rows: number }>;
  documents: Array<{ name: string; chunks: number }>;
  llm: LlmStatus;
  examples: string[];
};

type AiAnswer = {
  question: string;
  answer: string;
  mode: string;
  table: { columns: string[]; rows: Array<Array<string | number>> } | null;
  sources: string[];
  passages: Array<{ source: string; text: string; score: number }>;
  suggestions: string[];
  llm?: LlmStatus;
  error?: boolean;
};

const MODE_LABELS: Record<string, string> = {
  dataset: 'Computed from datasets',
  documents: 'Found in uploaded documents',
  'dataset+llm': 'Datasets, phrased by the language model',
  'documents+llm': 'Documents, phrased by the language model',
  llm: 'Language model, using dataset summaries',
  help: 'No match',
  error: 'Error'
};

function AnswerCard({ item }: { item: AiAnswer }) {
  return (
    <div className="space-y-3 rounded-2xl border border-slate-200 bg-white p-5">
      <p className="text-sm font-semibold text-slate-500">Q: {item.question}</p>
      <div className="flex flex-wrap gap-2">
        <span className={`rounded-full px-3 py-1 text-xs font-semibold ${item.error ? 'bg-rose-100 text-rose-800' : item.mode === 'help' ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800'}`}>
          {MODE_LABELS[item.mode] ?? item.mode}
        </span>
        {item.sources.map((source) => (
          <span key={source} className="rounded-full bg-slate-100 px-3 py-1 font-mono text-xs text-slate-700">{source}</span>
        ))}
      </div>
      <p className="whitespace-pre-line text-slate-900">{item.answer}</p>
      {item.table && (
        <div className="overflow-x-auto rounded-xl border border-slate-200">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-slate-100 text-slate-700">
              <tr>{item.table.columns.map((column) => <th key={column} className="px-3 py-2 font-semibold">{column}</th>)}</tr>
            </thead>
            <tbody>
              {item.table.rows.slice(0, 40).map((row, index) => (
                <tr key={index} className="border-t border-slate-200">
                  {row.map((cell, cellIndex) => <td key={cellIndex} className="px-3 py-2">{String(cell)}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {item.passages.length > 0 && (
        <details className="text-sm text-slate-600">
          <summary className="cursor-pointer select-none">Matching document passages ({item.passages.length})</summary>
          <ul className="mt-2 space-y-2">
            {item.passages.map((passage, index) => (
              <li key={index} className="rounded-xl bg-slate-50 p-3">
                <span className="font-mono text-xs text-slate-500">{passage.source} · relevance {passage.score}</span>
                <p className="mt-1 whitespace-pre-line">{passage.text}</p>
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}

function AIAssistant() {
  const status = useApiData<AiStatus>('/ai/status');
  const [history, setHistory] = useState<AiAnswer[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');

  const submitQuestion = async (question: string) => {
    setLoading(true);
    try {
      const response = await queryAiAssistant({ question, top_k: 3 });
      setHistory((previous) => [response.data as AiAnswer, ...previous]);
    } catch (error) {
      const answer = getErrorMessage(error, 'Unable to reach the AI assistant. Is the backend running?');
      setHistory((previous) => [
        { question, answer, mode: 'error', table: null, sources: [], passages: [], suggestions: [], error: true },
        ...previous
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);
    setUploadMessage(`Uploading and indexing ${file.name}…`);
    try {
      const response = await uploadAiDocument(formData);
      setUploadMessage(`${response.data.filename} indexed: ${response.data.chunks_indexed} chunks. You can now ask questions about it.`);
      status.reload();
    } catch (error) {
      setUploadMessage(`Upload failed: ${getErrorMessage(error, 'please try again.')}`);
    } finally {
      setLoading(false);
    }
  };

  // The latest answer carries the freshest model status (e.g. after OpenAI reports no credits).
  const llm = history.find((item) => item.llm)?.llm ?? status.data?.llm;
  const examples = history[0]?.suggestions?.length ? history[0].suggestions : status.data?.examples ?? [];

  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">AI Assistant</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">PharmaIQ Analytics Assistant</h1>
      </header>

      <div className="grid gap-6 xl:grid-cols-[1.6fr_1fr]">
        <div className="space-y-6">
          <ChatInterface onSubmit={submitQuestion} loading={loading} />
          <div className="flex flex-wrap gap-2">
            {examples.map((example) => (
              <button
                key={example}
                disabled={loading}
                onClick={() => submitQuestion(example)}
                className="rounded-full border border-slate-300 bg-white px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-100 disabled:opacity-50"
              >
                {example}
              </button>
            ))}
          </div>
          {loading && <p className="text-sm text-slate-500">Working on it… (the first question after starting the API can take up to a minute while the AI model loads)</p>}
          <section className="space-y-4">
            {history.map((item, index) => <AnswerCard key={index} item={item} />)}
            {!history.length && <p className="text-slate-500">Ask a question or click an example above.</p>}
          </section>
        </div>

        <div className="space-y-6">
          <DocumentUpload onUpload={handleUpload} />
          {uploadMessage && <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">{uploadMessage}</div>}

          <section className="space-y-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">What the assistant knows</h2>
            {status.error && <p className="text-sm text-rose-700">{status.error}</p>}
            {status.data && (
              <>
                <div>
                  <p className="text-sm font-semibold text-slate-700">Datasets (answers computed live)</p>
                  <ul className="mt-1 space-y-1 text-sm text-slate-600">
                    {status.data.datasets.map((dataset) => (
                      <li key={dataset.name}><span className="font-mono">{dataset.name}</span> · {dataset.rows.toLocaleString()} rows</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-700">Uploaded documents (searched by meaning)</p>
                  <ul className="mt-1 space-y-1 text-sm text-slate-600">
                    {status.data.documents.map((document) => (
                      <li key={document.name}>
                        <span className="font-mono">{document.name}</span> · {document.chunks ? `${document.chunks} chunks` : 'indexed on first question'}
                      </li>
                    ))}
                    {!status.data.documents.length && <li>None yet. Upload a PDF, TXT or CSV.</li>}
                  </ul>
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-700">Language model</p>
                  <p className="mt-1 text-sm text-slate-600">
                    {llm?.state === 'ready'
                      ? `${llm.provider} (${llm.model}) is configured and will phrase answers.`
                      : llm?.state === 'not configured'
                        ? 'No language model configured. Answers are computed directly from the data.'
                        : `${llm?.provider ?? 'The language model'} is unavailable (${llm?.last_error ?? 'unknown error'}). Answers are computed directly from the data.`}
                  </p>
                </div>
              </>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}

export default AIAssistant;
