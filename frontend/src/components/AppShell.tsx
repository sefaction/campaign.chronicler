import React from 'react';
import TopNav from './TopNav';
import CampaignSidebar from './CampaignSidebar';

type Props = { children: React.ReactNode };
export default function AppShell({ children }: Props) {
  return (
    <div className='app-root'>
      <TopNav />
      <div className='layout'>
        <CampaignSidebar />
        <main className='main-content'>{children}</main>
      </div>
    </div>
  );
}
