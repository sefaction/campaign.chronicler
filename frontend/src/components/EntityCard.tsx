import React from 'react';
import { Link } from 'react-router-dom';
import VisibilityBadge from './VisibilityBadge';
import TypeBadge from './TypeBadge';

export default function EntityCard({e}:{e:any}){return <article className='entity-card'><div className='avatar'>{(e.name||'?').slice(0,1)}</div><div><h3><Link to={`/entity/${e.id}`}>{e.name}</Link></h3><TypeBadge value={e.entity_type}/><p>{e.summary||'No summary'}</p><VisibilityBadge value={e.visibility}/><small>Updated: {e.updated_at||'n/a'}</small></div><div><Link to={`/entity/${e.id}`}>View</Link> · <Link to={`/entity/edit/${e.id}`}>Edit</Link></div></article>}
