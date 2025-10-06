"""Initial migration to create tables based on existing schema

Revision ID: initial_migration
Revises: 
Create Date: 2025-08-27 14:15:14.511193

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=50), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.current_timestamp())
    )

    # Create games table
    op.create_table('games',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('target_word', sa.String(length=5), nullable=False),
        sa.Column('status', sa.String(length=20), default='in_progress'),
        sa.Column('attempts', sa.Integer, default=0),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.current_timestamp()),
        sa.Column('completed_at', sa.TIMESTAMP, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )

    # Create guesses table
    op.create_table('guesses',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('game_id', sa.Integer, nullable=False),
        sa.Column('guess_word', sa.String(length=5), nullable=False),
        sa.Column('position', sa.Integer, nullable=False),
        sa.Column('feedback', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.current_timestamp()),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'])
    )

    # Create indexes
    op.create_index('idx_users_username', 'users', ['username'])
    op.create_index('idx_games_user_id', 'games', ['user_id'])
    op.create_index('idx_games_status', 'games', ['status'])
    op.create_index('idx_guesses_game_id', 'guesses', ['game_id'])
    op.create_index('idx_guesses_game_position', 'guesses', ['game_id', 'position'])

def downgrade() -> None:
    # Drop indexes first
    op.drop_index('idx_guesses_game_position', 'guesses')
    op.drop_index('idx_guesses_game_id', 'guesses')
    op.drop_index('idx_games_status', 'games')
    op.drop_index('idx_games_user_id', 'games')
    op.drop_index('idx_users_username', 'users')
    
    # Drop tables in reverse order
    op.drop_table('guesses')
    op.drop_table('games')
    op.drop_table('users')
