"""add user_id to user_task

Revision ID: e5a6bd8020b7
Revises: 44ffdf7abeaf
Create Date: 2026-09-28 16:55:04.041232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5a6bd8020b7'
down_revision: Union[str, Sequence[str], None] = '44ffdf7abeaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
