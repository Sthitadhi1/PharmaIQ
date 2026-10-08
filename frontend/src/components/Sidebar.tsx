import { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { apiRoot } from '../services/api';

const navItems = [
  { label: 'Dashboard', path: '/' },
  { label: 'Executive Dashboard', path: '/executive' },
  { label: 'Patient Analytics', path: '/patients' },
  { label: 'Clinical Trials', path: '/clinical' },
  { label: 'Sales Intelligence', path: '/sales' },
  { label: 'Doctor Segmentation', path: '/doctors' },
  { label: 'AI Assistant', path: '/ai' },
  { label: 'Login & Tokens', path: '/login' }
];

// TC-01: live health check of the backend, re-checked every 10 seconds.
function ApiHealth() {
  const [status, setStatus] = useState<'checking' | 'healthy' | 'down'>('checking');

  useEffect(() => {
    const check = () =>
      fetch(`${apiRoot}/health`)
        .then((response) => response.json())
        .then((body) => setStatus(body.status === 'healthy' ? 'healthy' : 'down'))
        .catch(() => setStatus('down'));
    check();
    const timer = window.setInterval(check, 10000);
    return () => window.clearInterval(timer);
  }, []);

  const styles = {
    checking: 'bg-slate-100 text-slate-600',
    healthy: 'bg-emerald-100 text-emerald-800',
    down: 'bg-rose-100 text-rose-800'
  };
  const labels = { checking: 'Checking API…', healthy: 'API healthy', down: 'API not reachable' };

  return <p className={`mt-8 rounded-xl px-4 py-3 text-sm font-semibold ${styles[status]}`}>{labels[status]}</p>;
}

function Sidebar() {
  return (
    <aside className="w-72 min-h-screen bg-white border-r border-slate-200 p-6">
      <div className="mb-10">
        <h1 className="text-2xl font-semibold text-slate-900">PharmaIQ</h1>
        <p className="mt-2 text-sm text-slate-600">Life sciences analytics platform</p>
      </div>
      <nav className="space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `block rounded-xl px-4 py-3 text-sm font-medium ${
                isActive ? 'bg-slate-900 text-white' : 'text-slate-700 hover:bg-slate-100'
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
      <ApiHealth />
    </aside>
  );
}

export default Sidebar;
