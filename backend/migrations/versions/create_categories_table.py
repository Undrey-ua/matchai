"""create categories table

Revision ID: abc123def456
Revises: previous_revision
Create Date: 2024-03-21 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), unique=True, index=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True)
    )

def downgrade():
    op.drop_table('categories') 