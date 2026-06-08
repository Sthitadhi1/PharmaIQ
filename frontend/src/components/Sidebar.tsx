import { NavLink } from 'react-router-dom';

const navItems = [
  { label: 'Dashboard', path: '/' },
  { label: 'Executive Dashboard', path: '/executive' },
  { label: 'Patient Analytics', path: '/patients' },
  { label: 'Clinical Trials', path: '/clinical' },
  { label: 'Sales Intelligence', path: '/sales' },
  { label: 'Doctor Segmentation', path: '/doctors' },
  { label: 'AI Assistant', path: '/ai' }
];

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
    </aside>
  );
}

export default Sidebar;
