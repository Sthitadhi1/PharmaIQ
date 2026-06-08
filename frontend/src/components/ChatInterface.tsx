import { useState, FormEvent } from 'react';

type ChatInterfaceProps = {
  onSubmit: (question: string) => void;
  loading: boolean;
};

function ChatInterface({ onSubmit, loading }: ChatInterfaceProps) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!question.trim()) return;
    onSubmit(question.trim());
    setQuestion('');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-900">Ask the AI Assistant</h2>
      <textarea
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        placeholder="Type a business question or research query..."
        rows={5}
        className="w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-slate-900 outline-none transition focus:border-slate-400"
      />
      <button
        type="submit"
        disabled={loading}
        className="inline-flex items-center justify-center rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? 'Processing…' : 'Send Question'}
      </button>
    </form>
  );
}

export default ChatInterface;
