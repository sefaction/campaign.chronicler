import React, { useEffect, useMemo, useState } from 'react';
import { Link, Route, Routes, useNavigate, useParams } from 'react-router-dom';
import './App.css';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? `${window.location.protocol}//${window.location.hostname}:18000`;
const campaignId = 1;

function Placeholder({ t }: { t: string }) {
  return <div className='card'><h2>{t}</h2><p>This page is scaffolded and ready for implementation.</p></div>;
}

function LoginPage() {
  const [username, setU] = useState('gm');
  const [password, setP] = useState('gm');
  const [status, setS] = useState('');
  const nav = useNavigate();
  return <div className='card'><h2>Login</h2><form onSubmit={async e => { e.preventDefault(); const r = await fetch(`${API_BASE}/auth/login`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ username, password }) }); if (!r.ok) { setS('Login failed'); return; } setS('ok'); nav('/entities'); }}><input value={username} onChange={e => setU(e.target.value)} /><input type='password' value={password} onChange={e => setP(e.target.value)} /><button>Sign in</button></form><p>{status}</p><p><strong>API:</strong> {API_BASE}</p></div>;
}

function Entities() {
  const [items, setItems] = useState<any[]>([]); const [q, setQ] = useState(''); const [entityType, setType] = useState(''); const [visibility, setVis] = useState(''); const [confidence, setConf] = useState('');
  const load = () => fetch(`${API_BASE}/campaigns/${campaignId}/entities?q=${encodeURIComponent(q)}&entity_type=${entityType}&visibility=${visibility}&confidence=${confidence}&sort=name`).then(r => r.json()).then(setItems);
  useEffect(() => { load(); }, []);
  return <div className='card'><h2>Entities</h2><div className='toolbar'><input placeholder='search' value={q} onChange={e => setQ(e.target.value)} /><input placeholder='type' value={entityType} onChange={e => setType(e.target.value)} /><input placeholder='visibility' value={visibility} onChange={e => setVis(e.target.value)} /><input placeholder='confidence' value={confidence} onChange={e => setConf(e.target.value)} /><button onClick={load}>Apply</button><Link to='/entity/new'>New Entity</Link></div><ul>{items.map(i => <li key={i.id}><Link to={`/entity/${i.id}`}>{i.name}</Link> ({i.entity_type})</li>)}</ul></div>;
}

function EntityForm() {
  const { id } = useParams(); const edit = !!id && id !== 'new'; const [data, setData] = useState<any>({ campaign_id: 1, entity_type: 'character', name: '', summary: '', description_markdown: '', public_notes_markdown: '', rumor_notes_markdown: '', gm_notes_markdown: '', visibility: 'party', confidence: 'unknown', status: '' }); const nav = useNavigate();
  useEffect(() => { if (edit) fetch(`${API_BASE}/entities/${id}`).then(r => r.json()).then(setData); }, [id]);
  const save = async () => { const method = edit ? 'PUT' : 'POST'; const url = edit ? `${API_BASE}/entities/${id}` : `${API_BASE}/entities`; await fetch(url, { method, headers: { 'content-type': 'application/json' }, body: JSON.stringify(data) }); nav('/entities'); };
  return <div className='card'><h2>{edit ? 'Edit' : 'New'} Entity</h2>{['name', 'aliases', 'summary', 'status', 'entity_type', 'visibility', 'confidence', 'foundry_journal_uuid', 'foundry_actor_uuid', 'foundry_compendium_uuid'].map(k => <div key={k}><label>{k}<input value={data[k] || ''} onChange={e => setData({ ...data, [k]: e.target.value })} /></label></div>)}{['description_markdown', 'public_notes_markdown', 'rumor_notes_markdown', 'gm_notes_markdown'].map(k => <div key={k}><label>{k}<textarea value={data[k] || ''} onChange={e => setData({ ...data, [k]: e.target.value })} /></label></div>)}<button onClick={save}>Save</button></div>;
}

function EntityDetail() {
  const { id } = useParams(); const [d, setD] = useState<any>(); useEffect(() => { fetch(`${API_BASE}/entities/${id}/detail`).then(r => r.json()).then(setD); }, [id]); if (!d) return <div className='card'>Loading...</div>;
  return <div className='card'><h2>{d.entity.name}</h2><p>{d.entity.summary}</p><p>{d.entity.description_markdown}</p><p>Visibility: {d.entity.visibility} | Confidence: {d.entity.confidence}</p><h3>Tags</h3><ul>{d.tags.length ? d.tags.map((t: any) => <li key={t.id}>{t.name}</li>) : <li>No tags</li>}</ul><h3>Outgoing Relationships</h3><ul>{d.outgoing_relationships.length ? d.outgoing_relationships.map((r: any) => <li key={r.id}>{r.source_label || r.relationship_type}{' -> '}#{r.target_entity_id} ({r.status}/{r.confidence})</li>) : <li>No outgoing relationships</li>}</ul><h3>Incoming Relationships</h3><ul>{d.incoming_relationships.length ? d.incoming_relationships.map((r: any) => <li key={r.id}>#{r.source_entity_id} {r.target_label || r.relationship_type} ({r.status}/{r.confidence})</li>) : <li>No incoming relationships</li>}</ul><h3>Related Events</h3><ul>{d.related_events.length ? d.related_events.map((e: any) => <li key={e.id}>{e.title}</li>) : <li>No events</li>}</ul></div>;
}

export default function App() {
  const links = useMemo(() => ['login', 'campaigns', 'dashboard', 'entities', 'entity/new', 'entity/1', 'relationships', 'events', 'event/new', 'sessions', 'session/new', 'tags', 'calendars'], []);
  return <div className='shell'><aside className='sidebar'><h3>Campaign Chronicler</h3>{links.map(p => <div key={p}><Link to={'/' + p}>{p}</Link></div>)}</aside><main className='content'><Routes><Route path='/login' element={<LoginPage />} /><Route path='/campaigns' element={<Placeholder t='Campaign List' />} /><Route path='/dashboard' element={<Placeholder t='Campaign Dashboard' />} /><Route path='/entities' element={<Entities />} /><Route path='/entity/new' element={<EntityForm />} /><Route path='/entity/:id' element={<EntityDetail />} /><Route path='/entity/edit/:id' element={<EntityForm />} /><Route path='/relationships' element={<Placeholder t='Relationship CRUD via API ready' />} /><Route path='/events' element={<Placeholder t='Event CRUD via API ready' />} /><Route path='/event/new' element={<Placeholder t='Event Create/Edit' />} /><Route path='/sessions' element={<Placeholder t='Session List' />} /><Route path='/session/new' element={<Placeholder t='Session Create/Edit' />} /><Route path='/timelines' element={<Placeholder t='Timeline CRUD via API ready' />} /><Route path='/tags' element={<Placeholder t='Tag CRUD via API ready' />} /><Route path='/calendars' element={<Placeholder t='Calendar Settings' />} /><Route path='*' element={<LoginPage />} /></Routes></main></div>;
}
