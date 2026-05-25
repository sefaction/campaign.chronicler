import React from 'react';
export default function SearchBox({value,onChange}:{value:string;onChange:(v:string)=>void}){return <input placeholder='Search campaign' value={value} onChange={e=>onChange(e.target.value)} />}
