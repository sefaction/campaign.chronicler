import React from 'react';
import { Link } from 'react-router-dom';

export default function TopNav() {
  const links = ['Campaigns','Characters','Places','Organizations','Events','Timelines','Relationships','Tags','Settings'];
  return <header className='topnav'><div className='brand'>Campaign Chronicler</div><nav>{links.map(l=><Link key={l} to='/'>{l}</Link>)}</nav><div className='topnav-right'><button>☀/🌙</button><button>GM</button></div></header>;
}
