import { Link, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';

export default function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">FX PRICE INTELLIGENCE</div>
        <nav className="nav">
          <Link to="/">Dashboard</Link>
        </nav>
      </aside>
      <main className="main-panel">
        <Routes>
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </main>
    </div>
  );
}
