import React, { useEffect, useState } from 'react';
import { Link, Route, Routes, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import './App.css';
import AppShell from './components/AppShell';
import CampaignDashboard from './components/CampaignDashboard';
import EntityCard from './components/EntityCard';
import { api } from './api/client';

const campaignId = 1;
const Coming = ({t}:{t:string}) => <div className='card'><h2>{t}</h2><p>Coming later</p></div>;
const errMsg = (e:unknown)=> e instanceof Error ? e.message : String(e);

function LoginPage() { const [username,setU]=useState('gm');const [password,setP]=useState('gm');const [status,setS]=useState('');const nav=useNavigate(); return <div className='card'><h2>Login</h2><form onSubmit={async e=>{e.preventDefault();try{await api.login(username,password);nav('/entities');}catch(e){setS(errMsg(e));}}}><input value={username} onChange={e=>setU(e.target.value)}/><input type='password' value={password} onChange={e=>setP(e.target.value)}/><button>Sign in</button></form><p>{status}</p></div>; }

function Entities() {
  const [sp] = useSearchParams(); const [items,setItems]=useState<any[]>([]); const [q,setQ]=useState(sp.get('q')||''); const [entityType,setType]=useState(sp.get('entity_type')||''); const [visibility,setVis]=useState(sp.get('visibility')||''); const [confidence,setConf]=useState(sp.get('confidence')||''); const [tagId,setTag]=useState(sp.get('tag_id')||''); const [err,setErr]=useState('');
  const load=()=>api.listEntities(campaignId,{q,entity_type:entityType,visibility,confidence,tag_id:tagId,sort:'recent'}).then(setItems).catch(e=>setErr(errMsg(e)));
  useEffect(()=>{setQ(sp.get('q')||'');setType(sp.get('entity_type')||'');setVis(sp.get('visibility')||'');setConf(sp.get('confidence')||'');setTag(sp.get('tag_id')||'');},[sp]);
  useEffect(()=>{load();},[q,entityType,visibility,confidence,tagId]);
  return <CampaignDashboard><section className='card'><h2>Entity Records</h2><div className='toolbar'><input placeholder='search by name/summary' value={q} onChange={e=>setQ(e.target.value)} /><input placeholder='type' value={entityType} onChange={e=>setType(e.target.value)} /><input placeholder='visibility' value={visibility} onChange={e=>setVis(e.target.value)} /><input placeholder='confidence' value={confidence} onChange={e=>setConf(e.target.value)} /><input placeholder='tag id' value={tagId} onChange={e=>setTag(e.target.value)} /><button onClick={load}>Apply</button><Link to={`/entity/new?campaign_id=${campaignId}`}>New Entity</Link></div>{err&&<div className='error-panel'>{err}</div>}<div className='card-list'>{items.map(i=><EntityCard key={i.id} e={i} onDeleted={load} />)}</div></section></CampaignDashboard>;
}

function EntityForm() {
  const {id}=useParams(); const [sp]=useSearchParams(); const edit=!!id&&id!=='new'; const nav=useNavigate();
  const activeCampaignId = Number(sp.get('campaign_id') || campaignId);
  const [data,setData]=useState<any>({campaign_id:activeCampaignId,entity_type:'character',name:'',aliases:'',summary:'',description_markdown:'',public_notes_markdown:'',rumor_notes_markdown:'',gm_notes_markdown:'',visibility:'gm_only',confidence:'confirmed',status:'active'});
  const [err,setErr]=useState('');
  useEffect(()=>{ if(edit) api.getEntity(id!).then(setData).catch(e=>setErr(errMsg(e))); },[id]);
  const save=async(e:React.FormEvent)=>{ e.preventDefault(); setErr(''); try{ const payload={...data,campaign_id:data.campaign_id||activeCampaignId}; const res=edit?await api.updateEntity(id!,payload):await api.createEntity(payload); nav(`/entity/${res.id||id}`);}catch(e){setErr(errMsg(e));}};
  return <section className='card'><h2>{edit?'Edit':'New'} Entity</h2>{err&&<div className='error-panel'>{err}</div>}<p><strong>Campaign ID:</strong> {data.campaign_id}</p><form onSubmit={save}>{['name','aliases','summary','status','entity_type','visibility','confidence','foundry_journal_uuid','foundry_actor_uuid','foundry_compendium_uuid'].map(k=><div key={k}><label>{k}<input value={data[k]||''} onChange={e=>setData({...data,[k]:e.target.value})}/></label></div>)}{['description_markdown','public_notes_markdown','rumor_notes_markdown','gm_notes_markdown'].map(k=><div key={k}><label>{k}<textarea value={data[k]||''} onChange={e=>setData({...data,[k]:e.target.value})}/></label></div>)}<button type='submit'>Save</button><button type='button' onClick={()=>nav(-1)}>Cancel</button></form></section>;
}

function EntityDetail(){const {id}=useParams(); const [d,setD]=useState<any>(); useEffect(()=>{api.getEntityDetail(id!).then(setD);},[id]); if(!d) return <div className='card'>Loading...</div>; return <section className='card'><h1>{d.entity.name}</h1><p>{d.entity.summary}</p><p>{d.entity.description_markdown}</p><h3>GM Notes</h3><p>{d.entity.gm_notes_markdown||'None'}</p><h3>Rumor Notes</h3><p>{d.entity.rumor_notes_markdown||'None'}</p></section>;}

function ListPage({title,loader,createTo}:{title:string;loader:()=>Promise<any[]>;createTo?:string}){const [items,setItems]=useState<any[]>([]);const [err,setErr]=useState('');useEffect(()=>{loader().then(setItems).catch(e=>setErr(errMsg(e)));},[]);return <CampaignDashboard><div className='card'><h2>{title}</h2>{createTo&&<p><Link to={createTo}>New {title.slice(0,-1)}</Link></p>}{err&&<div className='error-panel'>{err}</div>}<ul>{items.map((i:any)=><li key={i.id||i.type}>{i.title||i.name||i.type}</li>)}</ul></div></CampaignDashboard>}
function FoundrySync(){const [s,setS]=useState<any>();useEffect(()=>{api.foundryStatus().then(setS);},[]);return <CampaignDashboard><div className='card'><h2>Foundry Sync</h2><pre>{JSON.stringify(s,null,2)}</pre></div></CampaignDashboard>}

export default function App(){return <AppShell><Routes><Route path='/login' element={<LoginPage/>}/><Route path='/campaigns' element={<CampaignDashboard><Coming t='Campaigns'/></CampaignDashboard>}/><Route path='/dashboard' element={<Entities/>}/><Route path='/entities' element={<Entities/>}/><Route path='/entity/new' element={<CampaignDashboard><EntityForm/></CampaignDashboard>}/><Route path='/entity/:id' element={<CampaignDashboard><EntityDetail/></CampaignDashboard>}/><Route path='/entity/edit/:id' element={<CampaignDashboard><EntityForm/></CampaignDashboard>}/><Route path='/relationships' element={<ListPage title='Relationships' loader={()=>api.listRelationships(campaignId)} createTo='/relationships/new'/>}/><Route path='/events' element={<ListPage title='Events' loader={()=>api.listEvents(campaignId)} createTo='/event/new'/>}/><Route path='/timelines' element={<ListPage title='Timelines' loader={()=>Promise.resolve([{id:1,name:'Main Timeline'}])} createTo='/timelines/new'/>}/><Route path='/tags' element={<ListPage title='Tags' loader={()=>api.listTags(campaignId)} createTo='/tags/new'/>}/><Route path='/sessions' element={<CampaignDashboard><Coming t='Sessions'/></CampaignDashboard>}/><Route path='/calendars' element={<CampaignDashboard><Coming t='Calendars / Settings'/></CampaignDashboard>}/><Route path='/settings' element={<CampaignDashboard><Coming t='Settings'/></CampaignDashboard>}/><Route path='/foundry-sync' element={<FoundrySync/>}/><Route path='*' element={<Entities/>}/></Routes></AppShell>}
