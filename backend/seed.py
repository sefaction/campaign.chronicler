from app.db.session import SessionLocal
from app.models import models as m

db=SessionLocal()
if not db.query(m.User).filter_by(username='gm').first():
    u=m.User(username='gm',password_hash='gm',display_name='Game Master',role=m.RoleEnum.gm); db.add(u); db.flush()
    c=m.Campaign(name='Shadows of Absalom',description='Example campaign',game_system='Pathfinder 2e'); db.add(c); db.flush()
    cal=m.Calendar(campaign_id=c.id,name='Golarion',calendar_type=m.CalendarType.golarion); db.add(cal); db.flush(); c.default_calendar_id=cal.id
    tl=m.Timeline(campaign_id=c.id,name='Main Timeline',visibility=m.Visibility.party,description='Campaign spine'); db.add(tl); db.flush()
    tags=[m.Tag(campaign_id=c.id,name='Nobility',color='#8844ff'),m.Tag(campaign_id=c.id,name='Faction',color='#44aa88'),m.Tag(campaign_id=c.id,name='Rumor',color='#eab308')]
    db.add_all(tags); db.flush()
    e1=m.Entity(campaign_id=c.id,entity_type=m.EntityType.character,name='Lady Virelle',summary='A scheming noble.',confidence=m.Confidence.confirmed)
    e2=m.Entity(campaign_id=c.id,entity_type=m.EntityType.settlement,name='Ivy District',summary='Affluent quarter.')
    e3=m.Entity(campaign_id=c.id,entity_type=m.EntityType.faction,name='Velvet Circle',summary='Secretive social ring.',confidence=m.Confidence.suspected)
    e4=m.Entity(campaign_id=c.id,entity_type=m.EntityType.character,name='Captain Orsik',summary='River captain.',confidence=m.Confidence.confirmed)
    db.add_all([e1,e2,e3,e4]); db.flush()
    db.add_all([m.EntityTag(entity_id=e1.id,tag_id=tags[0].id),m.EntityTag(entity_id=e3.id,tag_id=tags[1].id)])
    ev1=m.Event(campaign_id=c.id,timeline_id=tl.id,title='Masquerade Intrigue',calendar_id=cal.id,year_ar=4722,month_number=10,month_name='Lamashan',day=12,date_precision=m.DatePrecision.exact,display_date='12 Lamashan 4722 AR',sort_key=47221012,confidence=m.Confidence.confirmed)
    ev2=m.Event(campaign_id=c.id,timeline_id=tl.id,title='Dockside Riot',calendar_id=cal.id,year_ar=4722,month_number=11,month_name='Neth',day=4,date_precision=m.DatePrecision.exact,display_date='4 Neth 4722 AR',sort_key=47221104,confidence=m.Confidence.suspected)
    ev3=m.Event(campaign_id=c.id,timeline_id=tl.id,title='Winter Oath',calendar_id=cal.id,year_ar=4722,month_number=12,month_name='Kuthona',day=19,date_precision=m.DatePrecision.exact,display_date='19 Kuthona 4722 AR',sort_key=47221219,confidence=m.Confidence.confirmed)
    db.add_all([ev1,ev2,ev3]); db.flush()
    db.add_all([
      m.Relationship(campaign_id=c.id,source_entity_id=e1.id,target_entity_id=e3.id,relationship_type='leader_of',source_label='leader of',target_label='led by',confidence=m.Confidence.suspected),
      m.Relationship(campaign_id=c.id,source_entity_id=e3.id,target_entity_id=e2.id,relationship_type='located_in',source_label='located in',target_label='contains location'),
      m.Relationship(campaign_id=c.id,source_entity_id=e4.id,target_entity_id=e2.id,relationship_type='protects',source_label='protects',target_label='protected by'),
      m.Relationship(campaign_id=c.id,source_entity_id=e4.id,target_entity_id=e1.id,relationship_type='owes_debt_to',source_label='owes debt to',target_label='creditor of'),
      m.Relationship(campaign_id=c.id,source_entity_id=e1.id,target_entity_id=e4.id,relationship_type='betrayed',source_label='betrayed',target_label='betrayed by',confidence=m.Confidence.rumor)
    ])
    db.add_all([
      m.EventParticipant(event_id=ev1.id,entity_id=e1.id,role='participant'),
      m.EventParticipant(event_id=ev1.id,entity_id=e3.id,role='mentioned'),
      m.EventParticipant(event_id=ev2.id,entity_id=e4.id,role='participant'),
      m.EventParticipant(event_id=ev3.id,entity_id=e1.id,role='ally')
    ])
    db.commit()
print('Seeded.')
