"""add_current_game_id_to_users

Revision ID: 5ad7644389ae
Revises: initial_migration
Create Date: 2025-08-29 02:19:51.522106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ad7644389ae'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add current_game_id column to users table
    op.add_column('users', sa.Column('current_game_id', sa.Integer, sa.ForeignKey('games.id'), nullable=True))


def downgrade() -> None:
    # Remove current_game_id column from users table
    op.drop_column('users', 'current_game_id')
