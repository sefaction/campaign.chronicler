import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBox from './SearchBox';
import { api } from '../api/client';

export default function CampaignSidebar(){
  const [q,setQ]=useState('');
  const [tags,setTags]=useState<any[]>([]);
  const nav=useNavigate();
  useEffect(()=>{api.listTags(1).then(setTags).catch(()=>setTags([]));},[]);
  const items=[['Characters','/entities?entity_type=character'],['Places','/entities?entity_type=place'],['Organizations','/entities?entity_type=organization'],['Events','/events'],['Timelines','/timelines'],['Relationships','/relationships'],['Sessions','/sessions'],['Tags','/tags']];
  return <aside className='sidebar'><SearchBox value={q} onChange={setQ}/><button onClick={()=>nav(`/entities?q=${encodeURIComponent(q)}`)}>Search</button><div className='side-grid'>{items.map(([k,to])=><button key={k} className='side-btn' onClick={()=>nav(to)}>{k}</button>)}</div><h4>Visibility</h4><div className='chips'>{[['Public','public'],['Party','party'],['Specific Players','specific_players'],['GM Only','gm_only'],['Rumor','rumor']].map(([v,val])=><button key={v} className='chip' onClick={()=>nav(`/entities?visibility=${val}`)}>{v}</button>)}</div><h4>Tag Filters</h4><div className='chips'>{tags.length?tags.map((t:any)=><button className='chip' key={t.id} onClick={()=>nav(`/entities?tag_id=${t.id}`)}>{t.name}</button>):<span className='chip'>No tags yet</span>}</div><h4>Favorites</h4><div className='chips'><button className='chip'>Coming later</button></div></aside>
}
