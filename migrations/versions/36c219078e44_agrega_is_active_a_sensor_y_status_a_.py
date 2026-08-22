"""agrega is_active a sensor y status a alert

Revision ID: 36c219078e44
Revises: 8dbcc7f7df0b
Create Date: 2026-08-21 21:08:40.203212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36c219078e44'
down_revision: Union[str, Sequence[str], None] = '8dbcc7f7df0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'alert',
        sa.Column('status', sa.String(), nullable=False, server_default='open'),
    )
    op.add_column(
        'sensor',
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('sensor', 'is_active')
    op.drop_column('alert', 'status')