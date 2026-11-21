"""Add facility_policies table and policy reference for campus-specific policies

Revision ID: 002_add_campus_policies
Revises: 001_initial_schema
Create Date: 2026-11-21 15:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_add_campus_policies'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create facility_policies table
    op.create_table(
        'facility_policies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campus', sa.String(length=50), nullable=False),
        sa.Column('facility_type', sa.String(length=50), nullable=True),
        sa.Column('max_duration_minutes', sa.Integer(), nullable=False, server_default='180'),
        sa.Column('temp_threshold', sa.Float(), nullable=False, server_default='28.0'),
        sa.Column('requires_approval_for_restricted', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('policy_version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_facility_policies_id'), 'facility_policies', ['id'], unique=False)
    op.create_index(op.f('ix_facility_policies_campus'), 'facility_policies', ['campus'], unique=False)

    # Note: SQLite has limited ALTER TABLE support, so we use batch mode or add column
    with op.batch_alter_table('facilities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('policy_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_facilities_policy_id', 'facility_policies', ['policy_id'], ['id'])


def downgrade() -> None:
    with op.batch_alter_table('facilities', schema=None) as batch_op:
        batch_op.drop_constraint('fk_facilities_policy_id', type_='foreignkey')
        batch_op.drop_column('policy_id')
    op.drop_table('facility_policies')
