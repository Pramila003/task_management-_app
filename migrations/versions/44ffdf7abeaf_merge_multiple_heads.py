"""merge multiple heads

Revision ID: 44ffdf7abeaf
Revises: d30055a2ad65, fd5344578ba3
Create Date: 2026-09-28 16:53:38.744906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44ffdf7abeaf'
down_revision: Union[str, Sequence[str], None] = ('d30055a2ad65', 'fd5344578ba3')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
