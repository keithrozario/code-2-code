"""${message}"""
from alembic import op
import sqlalchemy as sa

revision = '${up_revision}'
down_revision = '${down_revision}'
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def upgrade():
    ${upgrade}

def downgrade():
    ${downgrade}