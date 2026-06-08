import { useState } from 'react';
import ChatInterface from '../components/ChatInterface';
import DocumentUpload from '../components/DocumentUpload';
import AIInsightCard from '../components/AIInsightCard';
import api, { uploadAiDocument } from '../services/api';

function AIAssistant() {
  const [history, setHistory] = useState<Array<{ question: string; answer: string }>>([]);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');

  const submitQuestion = async (question: string) => {
    setLoading(true);
    try {
      const response = await api.post('/ai/query', { question, top_k: 3 });
      const text = response.data?.answer || 'No response available';
      setHistory((prev) => [{ question, answer: text }, ...prev]);
      setAnswer(text);
    } catch (error) {
      setAnswer('Unable to retrieve AI answer.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);
    setUploadMessage('Uploading document...');
    try {
      await uploadAiDocument(formData);
      setUploadMessage('Document uploaded successfully.');
    } catch (error) {
      console.error(error);
      setUploadMessage('Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">AI Assistant</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">PharmaIQ Generative AI</h1>
      </header>

      <div className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <div className="space-y-6">
          <DocumentUpload onUpload={handleUpload} />
          {uploadMessage && (
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
              {uploadMessage}
            </div>
          )}
          <ChatInterface onSubmit={submitQuestion} loading={loading} />
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">Latest AI Answer</h2>
            <p className="mt-4 text-slate-700">{loading ? 'Waiting for response...' : answer || 'Ask a question to get started.'}</p>
          </div>
        </div>

        <div className="space-y-6">
          <AIInsightCard title="How it works" description="Upload clinical documents, then ask business or research questions to get AI-guided summaries and document intelligence." />
          <AIInsightCard title="Use cases" description="Clinical research analysis, sales region intelligence, drug document review, and executive insights." />
          <AIInsightCard title="Tip" description="Try: 'Which region generated maximum sales?' or 'Summarize clinical trial risk factors.'" />
        </div>
      </div>

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Conversation History</h2>
        <div className="mt-4 space-y-4">
          {history.map((item, index) => (
            <div key={index} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-semibold text-slate-700">Q: {item.question}</p>
              <p className="mt-2 text-slate-600">A: {item.answer}</p>
            </div>
          ))}
          {!history.length && <p className="text-slate-500">No questions asked yet.</p>}
        </div>
      </section>
    </div>
  );
}

export default AIAssistant;
