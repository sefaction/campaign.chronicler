import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Link, Route, Routes, useNavigate } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:18000';

const shellStyle: React.CSSProperties = {
  display: 'grid',
  gridTemplateColumns: '240px 1fr',
  minHeight: '100vh',
  fontFamily: 'Inter, system-ui, sans-serif',
  background: '#f3f4f6',
  color: '#111827'
};

const navStyle: React.CSSProperties = {
  background: '#111827',
  color: '#f9fafb',
  padding: '16px',
  borderRight: '1px solid #1f2937'
};

const cardStyle: React.CSSProperties = {
  background: '#ffffff',
  borderRadius: 12,
  padding: 20,
  boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
};

function Placeholder({ t }: { t: string }) {
  return <div style={cardStyle}><h2 style={{ marginTop: 0 }}>{t}</h2><p>This page is scaffolded and ready for implementation.</p></div>;
}

function LoginPage() {
  const [username, setUsername] = useState('gm');
  const [password, setPassword] = useState('gm');
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  async function onLogin(e: React.FormEvent) {
    e.preventDefault();
    setStatus('Logging in...');
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      if (!res.ok) {
        setStatus('Login failed. Check credentials.');
        return;
      }
      const data = await res.json();
      localStorage.setItem('campaign_token', data.token ?? '');
      localStorage.setItem('campaign_user', JSON.stringify(data.user ?? {}));
      setStatus('Login success.');
      navigate('/campaigns');
    } catch {
      setStatus(`Cannot reach backend at ${API_BASE}`);
    }
  }

  return (
    <div style={cardStyle}>
      <h2 style={{ marginTop: 0 }}>Login</h2>
      <p style={{ marginTop: 0 }}>Seed user defaults are prefilled (`gm` / `gm`).</p>
      <form onSubmit={onLogin} style={{ display: 'grid', gap: 12, maxWidth: 360 }}>
        <label>Username<input value={username} onChange={e => setUsername(e.target.value)} style={{ width: '100%', padding: 8, marginTop: 4 }} /></label>
        <label>Password<input type='password' value={password} onChange={e => setPassword(e.target.value)} style={{ width: '100%', padding: 8, marginTop: 4 }} /></label>
        <button type='submit' style={{ padding: 10, background: '#2563eb', color: 'white', border: 0, borderRadius: 8 }}>Sign in</button>
      </form>
      <p>{status}</p>
      <p><strong>API:</strong> {API_BASE}</p>
    </div>
  );
}

function App() {
  const links = useMemo(() => ['login', 'campaigns', 'dashboard', 'entities', 'entity/new', 'entity/1', 'relationships/new', 'events', 'event/new', 'sessions', 'session/new', 'tags', 'calendars'], []);
  return (
    <BrowserRouter>
      <div style={shellStyle}>
        <nav style={navStyle}>
          <h3 style={{ marginTop: 0 }}>Campaign Chronicler</h3>
          <div style={{ display: 'grid', gap: 6 }}>
            {links.map(p => <Link key={p} to={'/' + p} style={{ color: '#93c5fd' }}>{p}</Link>)}
          </div>
        </nav>
        <main style={{ padding: 24 }}>
          <Routes>
            <Route path='/login' element={<LoginPage />} />
            <Route path='/campaigns' element={<Placeholder t='Campaign List' />} />
            <Route path='/dashboard' element={<Placeholder t='Campaign Dashboard' />} />
            <Route path='/entities' element={<Placeholder t='Entity List + Filters' />} />
            <Route path='/entity/new' element={<Placeholder t='Entity Create/Edit Form' />} />
            <Route path='/entity/:id' element={<Placeholder t='Entity Detail' />} />
            <Route path='/relationships/new' element={<Placeholder t='Relationship Create/Edit Form' />} />
            <Route path='/events' element={<Placeholder t='Event Timeline View' />} />
            <Route path='/event/new' element={<Placeholder t='Event Create/Edit Form + Participants Search' />} />
            <Route path='/sessions' element={<Placeholder t='Session List' />} />
            <Route path='/session/new' element={<Placeholder t='Session Create/Edit Form' />} />
            <Route path='/tags' element={<Placeholder t='Tag Management' />} />
            <Route path='/calendars' element={<Placeholder t='Calendar Settings (Golarion)' />} />
            <Route path='*' element={<LoginPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
