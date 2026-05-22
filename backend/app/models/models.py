from datetime import datetime, date
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Date, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
import enum

class RoleEnum(str, enum.Enum): admin="admin"; gm="gm"; player="player"
class CampaignMemberRole(str, enum.Enum): owner="owner"; gm="gm"; player="player"; viewer="viewer"
class Visibility(str, enum.Enum): gm_only="gm_only"; party="party"; specific_players="specific_players"; public="public"; rumor="rumor"
class CalendarType(str, enum.Enum): golarion="golarion"; custom="custom"
class DatePrecision(str, enum.Enum): exact="exact"; month="month"; year="year"; approximate="approximate"; unknown="unknown"
class EntityType(str, enum.Enum): character="character"; organization="organization"; place="place"; item="item"; ship="ship"; family="family"; deity="deity"; concept="concept"
class SyncStatus(str, enum.Enum): not_synced="not_synced"; synced="synced"; changed_local="changed_local"; changed_foundry="changed_foundry"; conflict="conflict"

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    username: Mapped[str]=mapped_column(String(64), unique=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    display_name: Mapped[str]=mapped_column(String(120))
    role: Mapped[RoleEnum]=mapped_column(Enum(RoleEnum), default=RoleEnum.player)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Campaign(Base):
    __tablename__="campaigns"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(150))
    description: Mapped[str|None]=mapped_column(Text)
    game_system: Mapped[str|None]=mapped_column(String(80))
    default_calendar_id: Mapped[int|None]=mapped_column(ForeignKey("calendars.id"))
    foundry_world_id: Mapped[str|None]=mapped_column(String(120))
    foundry_world_name: Mapped[str|None]=mapped_column(String(120))
    foundry_base_url: Mapped[str|None]=mapped_column(String(255))
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CampaignMember(Base):
    __tablename__="campaign_members"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id"))
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    role: Mapped[CampaignMemberRole]=mapped_column(Enum(CampaignMemberRole), default=CampaignMemberRole.player)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Calendar(Base):
    __tablename__="calendars"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id"))
    name: Mapped[str]=mapped_column(String(120))
    calendar_type: Mapped[CalendarType]=mapped_column(Enum(CalendarType), default=CalendarType.golarion)
    description: Mapped[str|None]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Entity(Base):
    __tablename__="entities"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id"))
    entity_type: Mapped[EntityType]=mapped_column(Enum(EntityType))
    name: Mapped[str]=mapped_column(String(150))
    aliases: Mapped[str|None]=mapped_column(Text)
    summary: Mapped[str|None]=mapped_column(Text)
    description_markdown: Mapped[str|None]=mapped_column(Text)
    gm_notes_markdown: Mapped[str|None]=mapped_column(Text)
    visibility: Mapped[Visibility]=mapped_column(Enum(Visibility), default=Visibility.party)
    status: Mapped[str|None]=mapped_column(String(60))
    image_url: Mapped[str|None]=mapped_column(String(255))
    foundry_journal_uuid: Mapped[str|None]=mapped_column(String(200))
    foundry_actor_uuid: Mapped[str|None]=mapped_column(String(200))
    foundry_compendium_uuid: Mapped[str|None]=mapped_column(String(200))
    sync_status: Mapped[SyncStatus]=mapped_column(Enum(SyncStatus), default=SyncStatus.not_synced)
    last_synced_at: Mapped[datetime|None]=mapped_column(DateTime)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Tag(Base):
    __tablename__="tags"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id"))
    name: Mapped[str]=mapped_column(String(80))
    color: Mapped[str|None]=mapped_column(String(20))
    description: Mapped[str|None]=mapped_column(Text)

class EntityTag(Base):
    __tablename__="entity_tags"
    entity_id: Mapped[int]=mapped_column(ForeignKey("entities.id"), primary_key=True)
    tag_id: Mapped[int]=mapped_column(ForeignKey("tags.id"), primary_key=True)

class Timeline(Base):
    __tablename__="timelines"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id"))
    name: Mapped[str]=mapped_column(String(120))
    description: Mapped[str|None]=mapped_column(Text)
    visibility: Mapped[Visibility]=mapped_column(Enum(Visibility), default=Visibility.party)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Event(Base):
    __tablename__="events"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id"))
    timeline_id: Mapped[int|None]=mapped_column(ForeignKey("timelines.id"))
    title: Mapped[str]=mapped_column(String(150))
    summary: Mapped[str|None]=mapped_column(Text)
    description_markdown: Mapped[str|None]=mapped_column(Text)
    gm_notes_markdown: Mapped[str|None]=mapped_column(Text)
    calendar_id: Mapped[int|None]=mapped_column(ForeignKey("calendars.id"))
    year_ar: Mapped[int|None]=mapped_column(Integer)
    month_number: Mapped[int|None]=mapped_column(Integer)
    month_name: Mapped[str|None]=mapped_column(String(40))
    day: Mapped[int|None]=mapped_column(Integer)
    date_precision: Mapped[DatePrecision]=mapped_column(Enum(DatePrecision), default=DatePrecision.unknown)
    display_date: Mapped[str|None]=mapped_column(String(80))
    sort_key: Mapped[int|None]=mapped_column(Integer)
    visibility: Mapped[Visibility]=mapped_column(Enum(Visibility), default=Visibility.party)
    location_entity_id: Mapped[int|None]=mapped_column(ForeignKey("entities.id"))
    foundry_journal_uuid: Mapped[str|None]=mapped_column(String(200))
    sync_status: Mapped[SyncStatus]=mapped_column(Enum(SyncStatus), default=SyncStatus.not_synced)
    last_synced_at: Mapped[datetime|None]=mapped_column(DateTime)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Relationship(Base):
    __tablename__="relationships"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id"))
    source_entity_id: Mapped[int]=mapped_column(ForeignKey("entities.id"))
    target_entity_id: Mapped[int]=mapped_column(ForeignKey("entities.id"))
    relationship_type: Mapped[str]=mapped_column(String(80))
    relationship_label: Mapped[str|None]=mapped_column(String(120))
    description_markdown: Mapped[str|None]=mapped_column(Text)
    gm_notes_markdown: Mapped[str|None]=mapped_column(Text)
    directionality: Mapped[str]=mapped_column(String(20), default="directed")
    status: Mapped[str]=mapped_column(String(20), default="active")
    confidence: Mapped[str]=mapped_column(String(20), default="confirmed")
    visibility: Mapped[Visibility]=mapped_column(Enum(Visibility), default=Visibility.party)
    start_year_ar: Mapped[int|None]=mapped_column(Integer)
    start_month_number: Mapped[int|None]=mapped_column(Integer)
    start_day: Mapped[int|None]=mapped_column(Integer)
    start_date_precision: Mapped[DatePrecision]=mapped_column(Enum(DatePrecision), default=DatePrecision.unknown)
    end_year_ar: Mapped[int|None]=mapped_column(Integer)
    end_month_number: Mapped[int|None]=mapped_column(Integer)
    end_day: Mapped[int|None]=mapped_column(Integer)
    end_date_precision: Mapped[DatePrecision]=mapped_column(Enum(DatePrecision), default=DatePrecision.unknown)
    start_event_id: Mapped[int|None]=mapped_column(ForeignKey("events.id"))
    end_event_id: Mapped[int|None]=mapped_column(ForeignKey("events.id"))
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EventParticipant(Base):
    __tablename__="event_participants"
    id: Mapped[int]=mapped_column(primary_key=True)
    event_id: Mapped[int]=mapped_column(ForeignKey("events.id"))
    entity_id: Mapped[int]=mapped_column(ForeignKey("entities.id"))
    role: Mapped[str]=mapped_column(String(20), default="participant")
    notes_markdown: Mapped[str|None]=mapped_column(Text)
    visibility: Mapped[Visibility]=mapped_column(Enum(Visibility), default=Visibility.party)

class Session(Base):
    __tablename__="sessions"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id"))
    session_number: Mapped[int|None]=mapped_column(Integer)
    real_world_date: Mapped[date|None]=mapped_column(Date)
    title: Mapped[str]=mapped_column(String(150))
    recap_markdown: Mapped[str|None]=mapped_column(Text)
    gm_notes_markdown: Mapped[str|None]=mapped_column(Text)
    visibility: Mapped[Visibility]=mapped_column(Enum(Visibility), default=Visibility.party)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SessionEntity(Base):
    __tablename__="session_entities"
    id: Mapped[int]=mapped_column(primary_key=True)
    session_id: Mapped[int]=mapped_column(ForeignKey("sessions.id"))
    entity_id: Mapped[int]=mapped_column(ForeignKey("entities.id"))
    role: Mapped[str|None]=mapped_column(String(50))
    notes_markdown: Mapped[str|None]=mapped_column(Text)
