import { Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import DashboardHome from './pages/DashboardHome';
import PatientAnalytics from './pages/PatientAnalytics';
import ClinicalTrials from './pages/ClinicalTrials';
import SalesIntelligence from './pages/SalesIntelligence';
import DoctorSegmentation from './pages/DoctorSegmentation';

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<DashboardHome />} />
            <Route path="/patients" element={<PatientAnalytics />} />
            <Route path="/clinical" element={<ClinicalTrials />} />
            <Route path="/sales" element={<SalesIntelligence />} />
            <Route path="/doctors" element={<DoctorSegmentation />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
