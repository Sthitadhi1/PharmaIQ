import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';

const salesForecastData = [
  { month: 'Jan', actual: 420, forecast: 430, variance: 2.4 },
  { month: 'Feb', actual: 540, forecast: 535, variance: -0.9 },
  { month: 'Mar', actual: 610, forecast: 620, variance: 1.6 },
  { month: 'Apr', actual: 720, forecast: 710, variance: -1.4 },
  { month: 'May', actual: 650, forecast: 665, variance: 2.3 },
  { month: 'Jun', forecast: 780, variance: 1.2 }
];

const productForecast = [
  { product: 'Drug A', current: 180, forecast: 215, growth: '19%' },
  { product: 'Drug B', current: 152, forecast: 172, growth: '13%' },
  { product: 'Drug C', current: 98, forecast: 115, growth: '17%' },
  { product: 'Drug D', current: 65, forecast: 78, growth: '20%' }
];

const regionPerformance = [
  { region: 'North', q1: 120, q2: 145, q3: 168, q4: 192 },
  { region: 'South', q1: 100, q2: 118, q3: 135, q4: 155 },
  { region: 'East', q1: 145, q2: 168, q3: 185, q4: 210 },
  { region: 'West', q1: 85, q2: 102, q3: 120, q4: 140 }
];

function SalesAnalytics() {
  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Commercial Intelligence</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Sales Forecasting & Analytics</h1>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        <MetricCard title="Forecast Accuracy" value="89%" subtitle="Model confidence" />
        <MetricCard title="Expected Growth" value="+16%" subtitle="Next quarter projection" />
        <MetricCard title="Stock Recommendation" value="28,500" subtitle="Units suggested" />
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Sales Forecast vs Actual">
          <ResponsiveContainer width="100%" height={280}>
            <AreaChart data={salesForecastData}>
              <defs>
                <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area type="monotone" dataKey="actual" stroke="#10b981" fill="#10b981" name="Actual Sales" />
              <Area type="monotone" dataKey="forecast" stroke="#3b82f6" fillOpacity={1} fill="url(#colorForecast)" name="Forecast" />
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Product-wise Forecast">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={productForecast}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="product" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="current" fill="#8b5cf6" name="Current Sales" />
              <Bar dataKey="forecast" fill="#3b82f6" name="Forecasted Sales" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Regional Quarterly Performance">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={regionPerformance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="q1" stroke="#ef4444" strokeWidth={2} name="Q1" />
              <Line type="monotone" dataKey="q2" stroke="#f59e0b" strokeWidth={2} name="Q2" />
              <Line type="monotone" dataKey="q3" stroke="#3b82f6" strokeWidth={2} name="Q3" />
              <Line type="monotone" dataKey="q4" stroke="#10b981" strokeWidth={2} name="Q4" />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Forecast Confidence">
          <div className="space-y-4 p-4">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-slate-700">High Confidence</span>
                <span className="text-xs text-slate-600">Products with {'<'} 10% variance</span>
              </div>
              <div className="mt-2 h-3 rounded-full bg-slate-200">
                <div className="h-full w-4/5 rounded-full bg-green-500"></div>
              </div>
              <p className="mt-1 text-sm text-slate-600">80%</p>
            </div>
            <div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-slate-700">Medium Confidence</span>
                <span className="text-xs text-slate-600">Products with 10-20% variance</span>
              </div>
              <div className="mt-2 h-3 rounded-full bg-slate-200">
                <div className="h-full w-3/5 rounded-full bg-yellow-500"></div>
              </div>
              <p className="mt-1 text-sm text-slate-600">60%</p>
            </div>
            <div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-slate-700">Low Confidence</span>
                <span className="text-xs text-slate-600">Products with {'>'} 20% variance</span>
              </div>
              <div className="mt-2 h-3 rounded-full bg-slate-200">
                <div className="h-full w-1/4 rounded-full bg-red-500"></div>
              </div>
              <p className="mt-1 text-sm text-slate-600">25%</p>
            </div>
          </div>
        </ChartCard>
      </div>
    </div>
  );
}

export default SalesAnalytics;
