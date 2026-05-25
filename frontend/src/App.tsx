import React, { useEffect, useState } from 'react';
import { Link, Route, Routes, useNavigate, useParams } from 'react-router-dom';
import './App.css';
import AppShell from './components/AppShell';
import CampaignDashboard from './components/CampaignDashboard';
import EntityCard from './components/EntityCard';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? `${window.location.protocol}//${window.location.hostname}:18000`;
const campaignId = 1;

function LoginPage() {
  const [username, setU] = useState('gm'); const [password, setP] = useState('gm'); const [status, setS] = useState(''); const nav = useNavigate();
  return <div className='card'><h2>Login</h2><form onSubmit={async e => { e.preventDefault(); const r = await fetch(`${API_BASE}/auth/login`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ username, password }) }); if (!r.ok) { setS('Login failed'); return; } nav('/entities'); }}><input value={username} onChange={e => setU(e.target.value)} /><input type='password' value={password} onChange={e => setP(e.target.value)} /><button>Sign in</button></form><p>{status}</p></div>;
}

function Entities() {
  const [items, setItems] = useState<any[]>([]); const [q, setQ] = useState(''); const [entityType, setType] = useState(''); const [visibility, setVis] = useState(''); const [confidence, setConf] = useState('');
  const load = () => fetch(`${API_BASE}/campaigns/${campaignId}/entities?q=${encodeURIComponent(q)}&entity_type=${entityType}&visibility=${visibility}&confidence=${confidence}&sort=recent`).then(r => r.json()).then(setItems);
  useEffect(() => { load(); }, []);
  return <CampaignDashboard><section className='card'><h2>Entity Records</h2><div className='toolbar'><input placeholder='search by name/summary' value={q} onChange={e => setQ(e.target.value)} /><input placeholder='type' value={entityType} onChange={e => setType(e.target.value)} /><input placeholder='visibility' value={visibility} onChange={e => setVis(e.target.value)} /><input placeholder='confidence' value={confidence} onChange={e => setConf(e.target.value)} /><button onClick={load}>Apply</button><Link to='/entity/new'>New Entity</Link></div><div className='card-list'>{items.map(i => <EntityCard key={i.id} e={i} />)}</div></section></CampaignDashboard>;
}

function EntityForm() {
  const { id } = useParams(); const edit = !!id && id !== 'new'; const [data, setData] = useState<any>({ campaign_id: 1, entity_type: 'character', name: '', summary: '', description_markdown: '', public_notes_markdown: '', rumor_notes_markdown: '', gm_notes_markdown: '', visibility: 'party', confidence: 'unknown', status: '' }); const nav = useNavigate();
  useEffect(() => { if (edit) fetch(`${API_BASE}/entities/${id}`).then(r => r.json()).then(setData); }, [id]);
  const save = async () => { const method = edit ? 'PUT' : 'POST'; const url = edit ? `${API_BASE}/entities/${id}` : `${API_BASE}/entities`; await fetch(url, { method, headers: { 'content-type': 'application/json' }, body: JSON.stringify(data) }); nav('/entities'); };
  return <section className='card'><h2>{edit ? 'Edit' : 'New'} Entity</h2>{['name', 'aliases', 'summary', 'status', 'entity_type', 'visibility', 'confidence', 'foundry_journal_uuid', 'foundry_actor_uuid', 'foundry_compendium_uuid'].map(k => <div key={k}><label>{k}<input value={data[k] || ''} onChange={e => setData({ ...data, [k]: e.target.value })} /></label></div>)}{['description_markdown', 'public_notes_markdown', 'rumor_notes_markdown', 'gm_notes_markdown'].map(k => <div key={k}><label>{k}<textarea value={data[k] || ''} onChange={e => setData({ ...data, [k]: e.target.value })} /></label></div>)}<button onClick={save}>Save</button></section>;
}

function EntityDetail() {
  const { id } = useParams(); const [d, setD] = useState<any>(); useEffect(() => { fetch(`${API_BASE}/entities/${id}/detail`).then(r => r.json()).then(setD); }, [id]); if (!d) return <div className='card'>Loading...</div>;
  return <section className='card'><h1>{d.entity.name}</h1><div className='detail-grid'><div><p>{d.entity.summary}</p><p>{d.entity.description_markdown}</p><h3>Relationships</h3><ul>{d.outgoing_relationships.length ? d.outgoing_relationships.map((r: any) => <li key={r.id}>{r.source_label || r.relationship_type}{' -> '}#{r.target_entity_id} ({r.status}/{r.confidence})</li>) : <li>No outgoing relationships</li>}</ul><ul>{d.incoming_relationships.length ? d.incoming_relationships.map((r: any) => <li key={r.id}>#{r.source_entity_id} {r.target_label || r.relationship_type} ({r.status}/{r.confidence})</li>) : <li>No incoming relationships</li>}</ul></div><aside><h3>Metadata</h3><p>Type: {d.entity.entity_type}</p><p>Visibility: {d.entity.visibility}</p><p>Confidence: {d.entity.confidence}</p><p>Status: {d.entity.status || 'n/a'}</p><h4>Foundry</h4><p>Journal: {d.entity.foundry_journal_uuid || '-'}</p></aside></div></section>;
}

function Wrap({children}:{children:React.ReactNode}){return <CampaignDashboard>{children}</CampaignDashboard>}

export default function App() {
  return <AppShell><Routes><Route path='/login' element={<LoginPage />} /><Route path='/campaigns' element={<Wrap><div className='card'><h2>Campaigns</h2></div></Wrap>} /><Route path='/dashboard' element={<Entities />} /><Route path='/entities' element={<Entities />} /><Route path='/entity/new' element={<Wrap><EntityForm /></Wrap>} /><Route path='/entity/:id' element={<Wrap><EntityDetail /></Wrap>} /><Route path='/entity/edit/:id' element={<Wrap><EntityForm /></Wrap>} /><Route path='/relationships' element={<Wrap><div className='card'><h2>Relationships</h2></div></Wrap>} /><Route path='/events' element={<Wrap><div className='card'><h2>Events</h2></div></Wrap>} /><Route path='/timelines' element={<Wrap><div className='card'><h2>Timelines</h2></div></Wrap>} /><Route path='/tags' element={<Wrap><div className='card'><h2>Tags</h2></div></Wrap>} /><Route path='/sessions' element={<Wrap><div className='card'><h2>Sessions</h2></div></Wrap>} /><Route path='/calendars' element={<Wrap><div className='card'><h2>Calendars / Settings</h2></div></Wrap>} /><Route path='*' element={<Entities />} /></Routes></AppShell>;
}
