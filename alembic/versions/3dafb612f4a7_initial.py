"""initial

Revision ID: 3dafb612f4a7
Revises: 
Create Date: 2024-06-11 21:56:42.555865

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '3dafb612f4a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('balance', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.CheckConstraint('balance >= 0.00'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('uid', postgresql.UUID(), nullable=False),
    sa.Column('type', sa.Enum('WITHDRAW', 'DEPOSIT', name='transactiontype'), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('uid')
    )


def downgrade() -> None:
    op.drop_table('transactions')
    op.drop_table('users')
