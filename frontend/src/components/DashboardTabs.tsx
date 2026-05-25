import React from 'react';
export default function DashboardTabs(){return <div className='tabs'>{['Overview','Graph','Timeline','Map','Players','Sessions','Foundry Sync'].map(t=><button key={t}>{t}</button>)}</div>}
