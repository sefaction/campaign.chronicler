import React from 'react';
import CampaignHeroCard from './CampaignHeroCard';
import DashboardTabs from './DashboardTabs';

export default function CampaignDashboard({children}:{children:React.ReactNode}){return <div><div className='breadcrumb'>Home &gt; Campaigns &gt; Shadows of Absalom</div><CampaignHeroCard/><DashboardTabs/>{children}</div>}
