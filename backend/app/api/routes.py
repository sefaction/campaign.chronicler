from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.session import get_db
from app.models import models as m
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
GOLARION_MONTHS=["Abadius","Calistril","Pharast","Gozran","Desnus","Sarenith","Erastus","Arodus","Rova","Lamashan","Neth","Kuthona"]

REL_TYPE_LABELS={"parent_of":("parent of","child of"),"child_of":("child of","parent of"),"sibling_of":("sibling of","sibling of"),"spouse_of":("spouse of","spouse of"),"lover_of":("lover of","lover of"),"ally_of":("ally of","ally of"),"enemy_of":("enemy of","enemy of"),"rival_of":("rival of","rival of"),"member_of":("member of","has member"),"leader_of":("leader of","led by"),"captain_of":("captain of","captained by"),"served_on":("served on","had crew"),"located_in":("located in","contains location"),"contains_location":("contains location","located in"),"rules":("rules","ruled by"),"ruled_by":("ruled by","rules"),"worships":("worships","patron of"),"patron_of":("patron of","worships"),"owns":("owns","owned by"),"created":("created","created by"),"destroyed":("destroyed","destroyed by"),"bound_to":("bound to","bound to"),"secretly_is":("secretly is","secretly is"),"killed_by":("killed by","killed"),"betrayed":("betrayed","betrayed by"),"protects":("protects","protected by"),"mentor_of":("mentor of","student of"),"student_of":("student of","mentor of"),"owes_debt_to":("owes debt to","creditor of")}

class LoginIn(BaseModel): username:str; password:str
@router.post('/auth/login')
def login(payload:LoginIn, db:Session=Depends(get_db)):
    user=db.query(m.User).filter(m.User.username==payload.username).first()
    if not user or user.password_hash!=payload.password: raise HTTPException(401,'invalid credentials')
    return {"token":"demo-token","user":{"id":user.id,"username":user.username,"role":user.role}}

@router.get('/relationship-types')
def relationship_types():
    return [{"type":k,"source_label":v[0],"target_label":v[1]} for k,v in REL_TYPE_LABELS.items()]

@router.get('/campaigns/{campaign_id}/entities')
def list_entities(campaign_id:int, q:str="", entity_type:Optional[str]=None, visibility:Optional[str]=None, confidence:Optional[str]=None, tag_id:Optional[int]=None, sort:str="name", db:Session=Depends(get_db)):
    qry=db.query(m.Entity).filter(m.Entity.campaign_id==campaign_id)
    if q:
        like=f"%{q}%"; qry=qry.filter(or_(m.Entity.name.ilike(like),m.Entity.aliases.ilike(like),m.Entity.summary.ilike(like),m.Entity.description_markdown.ilike(like)))
    if entity_type: qry=qry.filter(m.Entity.entity_type==entity_type)
    if visibility: qry=qry.filter(m.Entity.visibility==visibility)
    if confidence: qry=qry.filter(m.Entity.confidence==confidence)
    if tag_id: qry=qry.join(m.EntityTag,m.EntityTag.entity_id==m.Entity.id).filter(m.EntityTag.tag_id==tag_id)
    qry=qry.order_by(m.Entity.updated_at.desc() if sort=="recent" else m.Entity.entity_type.asc() if sort=="type" else m.Entity.name.asc())
    return qry.all()

@router.post('/entities')
def create_entity(payload:dict, db:Session=Depends(get_db)):
    tag_ids=payload.pop("tag_ids",[])
    obj=m.Entity(**payload); db.add(obj); db.commit(); db.refresh(obj)
    for tid in tag_ids: db.add(m.EntityTag(entity_id=obj.id,tag_id=tid))
    db.commit(); return obj

@router.get('/entities/{entity_id}')
def get_entity(entity_id:int, db:Session=Depends(get_db)):
    obj=db.get(m.Entity,entity_id)
    if not obj: raise HTTPException(404,'not found')
    return obj

@router.put('/entities/{entity_id}')
def update_entity(entity_id:int,payload:dict,db:Session=Depends(get_db)):
    obj=db.get(m.Entity,entity_id)
    if not obj: raise HTTPException(404,'not found')
    tag_ids=payload.pop("tag_ids",None)
    for k,v in payload.items(): setattr(obj,k,v)
    if tag_ids is not None:
        db.query(m.EntityTag).filter(m.EntityTag.entity_id==entity_id).delete()
        for tid in tag_ids: db.add(m.EntityTag(entity_id=entity_id, tag_id=tid))
    db.commit(); db.refresh(obj); return obj

@router.delete('/entities/{entity_id}')
def delete_entity(entity_id:int,db:Session=Depends(get_db)):
    db.query(m.EntityTag).filter(m.EntityTag.entity_id==entity_id).delete();
    obj=db.get(m.Entity,entity_id)
    if not obj: raise HTTPException(404,'not found')
    db.delete(obj); db.commit(); return {"ok":True}

@router.get('/entities/{entity_id}/detail')
def entity_detail(entity_id:int, db:Session=Depends(get_db)):
    e=db.get(m.Entity,entity_id)
    if not e: raise HTTPException(404,'not found')
    tags=db.query(m.Tag).join(m.EntityTag,m.EntityTag.tag_id==m.Tag.id).filter(m.EntityTag.entity_id==entity_id).all()
    outgoing=db.query(m.Relationship).filter(m.Relationship.source_entity_id==entity_id).all()
    incoming=db.query(m.Relationship).filter(m.Relationship.target_entity_id==entity_id).all()
    events=db.query(m.Event).join(m.EventParticipant,m.EventParticipant.event_id==m.Event.id).filter(m.EventParticipant.entity_id==entity_id).all()
    sessions=db.query(m.Session).join(m.SessionEntity,m.SessionEntity.session_id==m.Session.id).filter(m.SessionEntity.entity_id==entity_id).all()
    return {"entity":e,"tags":tags,"outgoing_relationships":outgoing,"incoming_relationships":incoming,"related_events":events,"related_sessions":sessions,"timeline_appearances":events}

# Tags CRUD
for n,mdl in [('campaigns',m.Campaign),('tags',m.Tag),('timelines',m.Timeline),('sessions',m.Session),('calendars',m.Calendar)]:
    r=APIRouter(prefix=f"/{n}")
    @r.get("")
    def _l(db:Session=Depends(get_db), _m=mdl): return db.query(_m).all()
    @r.post("")
    def _c(payload:dict, db:Session=Depends(get_db), _m=mdl): obj=_m(**payload); db.add(obj); db.commit(); db.refresh(obj); return obj
    @r.put('/{item_id}')
    def _u(item_id:int,payload:dict,db:Session=Depends(get_db), _m=mdl): obj=db.get(_m,item_id); [setattr(obj,k,v) for k,v in payload.items()]; db.commit(); db.refresh(obj); return obj
    @r.delete('/{item_id}')
    def _d(item_id:int,db:Session=Depends(get_db), _m=mdl): obj=db.get(_m,item_id); db.delete(obj); db.commit(); return {"ok":True}
    router.include_router(r)

@router.get('/campaigns/{campaign_id}/tags')
def tags_for_campaign(campaign_id:int, db:Session=Depends(get_db)): return db.query(m.Tag).filter(m.Tag.campaign_id==campaign_id).all()

@router.post('/relationships')
def create_relationship(payload:dict,db:Session=Depends(get_db)):
    tag_ids=payload.pop("tag_ids",[])
    if not payload.get('source_label') and payload.get('relationship_type') in REL_TYPE_LABELS: payload['source_label']=REL_TYPE_LABELS[payload['relationship_type']][0]
    if not payload.get('target_label') and payload.get('relationship_type') in REL_TYPE_LABELS: payload['target_label']=REL_TYPE_LABELS[payload['relationship_type']][1]
    obj=m.Relationship(**payload); db.add(obj); db.commit(); db.refresh(obj)
    for tid in tag_ids: db.add(m.RelationshipTag(relationship_id=obj.id, tag_id=tid))
    db.commit(); return obj

@router.get('/campaigns/{campaign_id}/relationships')
def list_relationships(campaign_id:int, db:Session=Depends(get_db)): return db.query(m.Relationship).filter(m.Relationship.campaign_id==campaign_id).all()
@router.put('/relationships/{rid}')
def update_relationship(rid:int,payload:dict,db:Session=Depends(get_db)): obj=db.get(m.Relationship,rid); [setattr(obj,k,v) for k,v in payload.items() if k!="tag_ids"]; db.commit(); db.refresh(obj); return obj
@router.delete('/relationships/{rid}')
def delete_relationship(rid:int,db:Session=Depends(get_db)): db.query(m.RelationshipTag).filter(m.RelationshipTag.relationship_id==rid).delete(); obj=db.get(m.Relationship,rid); db.delete(obj); db.commit(); return {"ok":True}

@router.post('/events')
def create_event(payload:dict,db:Session=Depends(get_db)):
    if payload.get('date_precision')=='exact' and payload.get('year_ar') and payload.get('month_number') and payload.get('day'):
        mn=payload['month_number']; payload['month_name']=payload.get('month_name') or (GOLARION_MONTHS[mn-1] if 1<=mn<=12 else None)
        payload['display_date']=f"{payload['day']} {payload['month_name']} {payload['year_ar']} AR"
        payload['sort_key']=int(f"{payload['year_ar']:04d}{mn:02d}{payload['day']:02d}")
    obj=m.Event(**payload); db.add(obj); db.commit(); db.refresh(obj); return obj
@router.get('/campaigns/{campaign_id}/events')
def list_events(campaign_id:int,db:Session=Depends(get_db)): return db.query(m.Event).filter(m.Event.campaign_id==campaign_id).order_by(m.Event.sort_key.asc().nullslast()).all()
@router.put('/events/{eid}')
def update_event(eid:int,payload:dict,db:Session=Depends(get_db)): obj=db.get(m.Event,eid); [setattr(obj,k,v) for k,v in payload.items()]; db.commit(); db.refresh(obj); return obj
@router.delete('/events/{eid}')
def delete_event(eid:int,db:Session=Depends(get_db)): obj=db.get(m.Event,eid); db.delete(obj); db.commit(); return {"ok":True}

@router.post('/event-participants')
def add_participant(payload:dict,db:Session=Depends(get_db)): obj=m.EventParticipant(**payload); db.add(obj); db.commit(); db.refresh(obj); return obj
@router.get('/events/{event_id}/participants')
def get_participants(event_id:int,db:Session=Depends(get_db)): return db.query(m.EventParticipant).filter(m.EventParticipant.event_id==event_id).all()

@router.get('/timelines/{timeline_id}/events')
def timeline_events(timeline_id:int, db:Session=Depends(get_db)):
    return db.query(m.Event).filter(m.Event.timeline_id==timeline_id).order_by(m.Event.sort_key.asc().nullslast()).all()

foundry=APIRouter(prefix='/foundry', tags=['foundry'])
@foundry.get('/status')
def foundry_status(): return {"status":"planned","message":"FoundryVTT sync is planned for a later phase."}
@foundry.post('/export-preview')
def export_preview(): return {"status":"planned","message":"Export preview is a placeholder; no Foundry API calls are made."}
@foundry.post('/import-preview')
def import_preview(): return {"status":"planned","message":"Import preview is a placeholder; no Foundry API calls are made."}
router.include_router(foundry)
