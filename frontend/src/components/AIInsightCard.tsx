type AIInsightCardProps = {
  title: string;
  description: string;
};

function AIInsightCard({ title, description }: AIInsightCardProps) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
      <p className="mt-3 text-slate-600">{description}</p>
    </div>
  );
}

export default AIInsightCard;
