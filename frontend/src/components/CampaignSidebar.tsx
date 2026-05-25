import React, { useState } from 'react';
import SearchBox from './SearchBox';

export default function CampaignSidebar(){
  const [q,setQ]=useState('');
  const items=[['Characters',0],['Places',0],['Organizations',0],['Events',0],['Timelines',0],['Relationships',0],['Sessions',0],['Tags',0]];
  return <aside className='sidebar'><SearchBox value={q} onChange={setQ}/><div className='side-grid'>{items.map(([k,c])=><button key={k} className='side-btn'>{k} <span>{c}</span></button>)}</div><h4>Visibility</h4><div className='chips'>{['Public','Party','Specific Players','GM Only','Rumor'].map(v=><span key={v} className='chip'>{v}</span>)}</div><h4>Tag Filters</h4><div className='chips'><span className='chip'>No tags yet</span></div><h4>Favorites</h4><div className='chips'><span className='chip'>Bookmarked placeholder</span></div></aside>
}
