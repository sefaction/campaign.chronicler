from app.db.session import SessionLocal
from app.models import models as m

db=SessionLocal()
if not db.query(m.User).filter_by(username='gm').first():
    u=m.User(username='gm',password_hash='gm',display_name='Game Master',role=m.RoleEnum.gm); db.add(u); db.flush()
    c=m.Campaign(name='Shadows of Absalom',description='Example campaign',game_system='Pathfinder 2e'); db.add(c); db.flush()
    cal=m.Calendar(campaign_id=c.id,name='Golarion',calendar_type=m.CalendarType.golarion); db.add(cal); db.flush(); c.default_calendar_id=cal.id
    t1=m.Tag(campaign_id=c.id,name='Nobility',color='#8844ff'); t2=m.Tag(campaign_id=c.id,name='Faction',color='#44aa88'); db.add_all([t1,t2]); db.flush()
    e1=m.Entity(campaign_id=c.id,entity_type=m.EntityType.character,name='Lady Virelle',summary='A scheming noble.'); e2=m.Entity(campaign_id=c.id,entity_type=m.EntityType.place,name='Ivy District',summary='Affluent quarter.'); db.add_all([e1,e2]); db.flush()
    db.add(m.EntityTag(entity_id=e1.id,tag_id=t1.id))
    tl=m.Timeline(campaign_id=c.id,name='Main Timeline'); db.add(tl); db.flush()
    ev=m.Event(campaign_id=c.id,timeline_id=tl.id,title='Masquerade Intrigue',calendar_id=cal.id,year_ar=4722,month_number=10,month_name='Lamashan',day=12,date_precision=m.DatePrecision.exact,display_date='12 Lamashan 4722 AR',sort_key=47221012); db.add(ev); db.flush()
    db.add(m.Relationship(campaign_id=c.id,source_entity_id=e1.id,target_entity_id=e2.id,relationship_type='located_in',relationship_label='Operates within'))
    s=m.Session(campaign_id=c.id,session_number=1,title='First Night in Absalom',recap_markdown='The party met Lady Virelle.'); db.add(s); db.flush(); db.add(m.SessionEntity(session_id=s.id,entity_id=e1.id,role='mentioned'))
    db.commit()
print('Seeded.')
