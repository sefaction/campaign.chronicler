import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import VisibilityBadge from './VisibilityBadge';
import TypeBadge from './TypeBadge';
import { api } from '../api/client';

export default function EntityCard({e,onDeleted}:{e:any;onDeleted:()=>void}){const nav=useNavigate();return <article className='entity-card'><div className='avatar'>{(e.name||'?').slice(0,1)}</div><div><h3><Link to={`/entity/${e.id}`}>{e.name}</Link></h3><button className='chip' onClick={()=>nav(`/entities?entity_type=${e.entity_type}`)}><TypeBadge value={e.entity_type}/></button><p>{e.summary||'No summary'}</p><button className='chip' onClick={()=>nav(`/entities?visibility=${e.visibility}`)}><VisibilityBadge value={e.visibility}/></button><small>Updated: {e.updated_at||'n/a'}</small></div><div><Link to={`/entity/${e.id}`}>View</Link> · <Link to={`/entity/edit/${e.id}`}>Edit</Link> · <button onClick={async()=>{if(confirm('Delete entity?')){await api.deleteEntity(e.id);onDeleted();}}}>Delete</button></div></article>}
