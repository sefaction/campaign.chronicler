from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.session import get_db
from app.models import models as m
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LoginIn(BaseModel): username:str; password:str
@router.post('/auth/login')
def login(payload:LoginIn, db:Session=Depends(get_db)):
    user=db.query(m.User).filter(m.User.username==payload.username).first()
    if not user or user.password_hash!=payload.password: raise HTTPException(401,'invalid credentials')
    return {"token":"demo-token","user":{"id":user.id,"username":user.username,"role":user.role}}

def crud_routes(name, model):
    r=APIRouter(prefix=f"/{name}", tags=[name])
    @r.get("")
    def list_items(db:Session=Depends(get_db)): return db.query(model).all()
    @r.post("")
    def create_item(payload:dict, db:Session=Depends(get_db)):
        obj=model(**payload); db.add(obj); db.commit(); db.refresh(obj); return obj
    @r.get('/{item_id}')
    def get_item(item_id:int, db:Session=Depends(get_db)):
        obj=db.get(model,item_id)
        if not obj: raise HTTPException(404,'not found')
        return obj
    @r.put('/{item_id}')
    def update_item(item_id:int,payload:dict,db:Session=Depends(get_db)):
        obj=db.get(model,item_id)
        if not obj: raise HTTPException(404,'not found')
        for k,v in payload.items(): setattr(obj,k,v)
        db.commit(); db.refresh(obj); return obj
    @r.delete('/{item_id}')
    def delete_item(item_id:int,db:Session=Depends(get_db)):
        obj=db.get(model,item_id)
        if not obj: raise HTTPException(404,'not found')
        db.delete(obj); db.commit(); return {"ok":True}
    return r

for n,mdl in [('campaigns',m.Campaign),('entities',m.Entity),('relationships',m.Relationship),('events',m.Event),('timelines',m.Timeline),('sessions',m.Session),('tags',m.Tag),('calendars',m.Calendar)]:
    router.include_router(crud_routes(n,mdl))

@router.get('/entities/filter')
def filter_entities(campaign_id:int, entity_type:Optional[str]=None, tag_id:Optional[int]=None, visibility:Optional[str]=None, status:Optional[str]=None, db:Session=Depends(get_db)):
    q=db.query(m.Entity).filter(m.Entity.campaign_id==campaign_id)
    if entity_type: q=q.filter(m.Entity.entity_type==entity_type)
    if visibility: q=q.filter(m.Entity.visibility==visibility)
    if status: q=q.filter(m.Entity.status==status)
    if tag_id: q=q.join(m.EntityTag,m.EntityTag.entity_id==m.Entity.id).filter(m.EntityTag.tag_id==tag_id)
    return q.all()

@router.get('/campaigns/{campaign_id}/search')
def search(campaign_id:int, q:str, db:Session=Depends(get_db)):
    like=f"%{q}%"
    return {
        'entities': db.query(m.Entity).filter(m.Entity.campaign_id==campaign_id).filter(or_(m.Entity.name.ilike(like),m.Entity.aliases.ilike(like),m.Entity.summary.ilike(like),m.Entity.description_markdown.ilike(like))).all(),
        'events': db.query(m.Event).filter(m.Event.campaign_id==campaign_id, m.Event.title.ilike(like)).all(),
        'sessions': db.query(m.Session).filter(m.Session.campaign_id==campaign_id, m.Session.recap_markdown.ilike(like)).all(),
    }

@router.get('/entities/{entity_id}/detail')
def entity_detail(entity_id:int, db:Session=Depends(get_db)):
    e=db.get(m.Entity,entity_id)
    if not e: raise HTTPException(404,'not found')
    tags=db.query(m.Tag).join(m.EntityTag,m.EntityTag.tag_id==m.Tag.id).filter(m.EntityTag.entity_id==entity_id).all()
    outgoing=db.query(m.Relationship).filter(m.Relationship.source_entity_id==entity_id).all()
    incoming=db.query(m.Relationship).filter(m.Relationship.target_entity_id==entity_id).all()
    events=db.query(m.Event).join(m.EventParticipant,m.EventParticipant.event_id==m.Event.id).filter(m.EventParticipant.entity_id==entity_id).all()
    sessions=db.query(m.Session).join(m.SessionEntity,m.SessionEntity.session_id==m.Session.id).filter(m.SessionEntity.entity_id==entity_id).all()
    return {"entity":e,"tags":tags,"outgoing_relationships":outgoing,"incoming_relationships":incoming,"related_events":events,"related_sessions":sessions}

@router.get('/timelines/{timeline_id}/events')
def timeline_events(timeline_id:int, db:Session=Depends(get_db)):
    return db.query(m.Event).filter(m.Event.timeline_id==timeline_id).order_by(m.Event.sort_key.asc()).all()

foundry=APIRouter(prefix='/foundry', tags=['foundry'])
@foundry.get('/status')
def foundry_status(): return {"status":"planned","message":"FoundryVTT sync is planned for a later phase."}
@foundry.post('/export-preview')
def export_preview(): return {"status":"planned","message":"Export preview is a placeholder; no Foundry API calls are made."}
@foundry.post('/import-preview')
def import_preview(): return {"status":"planned","message":"Import preview is a placeholder; no Foundry API calls are made."}
router.include_router(foundry)
