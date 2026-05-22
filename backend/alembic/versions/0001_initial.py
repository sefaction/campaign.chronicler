from alembic import op
import sqlalchemy as sa
from app.models.models import RoleEnum,CampaignMemberRole,Visibility,CalendarType,DatePrecision,EntityType,SyncStatus
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    from app.db.session import Base
    bind = op.get_bind()
    Base.metadata.create_all(bind)

def downgrade() -> None:
    from app.db.session import Base
    bind = op.get_bind()
    Base.metadata.drop_all(bind)
