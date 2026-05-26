import React from 'react';
import { NavLink } from 'react-router-dom';

export default function TopNav() {
  const links = [
    ['Campaigns','/campaigns'],['Characters','/entities?entity_type=character'],['Places','/entities?entity_type=place'],['Organizations','/entities?entity_type=organization'],['Events','/events'],['Timelines','/timelines'],['Relationships','/relationships'],['Tags','/tags'],['Settings','/settings']
  ];
  return <header className='topnav'><div className='brand'>Campaign Chronicler</div><nav>{links.map(([l,to])=><NavLink key={l} to={to}>{l}</NavLink>)}</nav><div className='topnav-right'><button title='Coming later'>☀/🌙</button><button title='Account placeholder'>GM</button></div></header>;
}
