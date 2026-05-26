import React from 'react';
import { NavLink } from 'react-router-dom';
export default function DashboardTabs(){return <div className='tabs'>{[['Overview','/campaigns'],['Entities','/entities'],['Relationships','/relationships'],['Timeline','/timelines'],['Sessions','/sessions'],['Foundry Sync','/foundry-sync']].map(([t,to])=><NavLink key={t} to={to}><button>{t}</button></NavLink>)}</div>}
