"""Initial database schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-11-21 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Facilities table
    op.create_table(
        'facilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=30), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('campus', sa.String(length=50), nullable=False, server_default='Main Campus'),
        sa.Column('building', sa.String(length=50), nullable=False),
        sa.Column('room_number', sa.String(length=20), nullable=False),
        sa.Column('facility_type', sa.String(length=50), nullable=False, server_default='General'),
        sa.Column('capacity', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('is_restricted', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_facilities_id'), 'facilities', ['id'], unique=False)
    op.create_index(op.f('ix_facilities_code'), 'facilities', ['code'], unique=True)

    # Bookings table
    op.create_table(
        'bookings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('booking_reference', sa.String(length=50), nullable=False),
        sa.Column('facility_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='CONFIRMED'),
        sa.Column('approved_by_user_id', sa.Integer(), nullable=True),
        sa.Column('approval_notes', sa.String(length=500), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['facility_id'], ['facilities.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['approved_by_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookings_id'), 'bookings', ['id'], unique=False)
    op.create_index(op.f('ix_bookings_booking_reference'), 'bookings', ['booking_reference'], unique=True)
    op.create_index(op.f('ix_bookings_facility_id'), 'bookings', ['facility_id'], unique=False)

    # Maintenance Tickets table
    op.create_table(
        'maintenance_tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticket_number', sa.String(length=50), nullable=False),
        sa.Column('facility_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, server_default='Facilities'),
        sa.Column('impact', sa.String(length=20), nullable=False),
        sa.Column('urgency', sa.String(length=20), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=False),
        sa.Column('state', sa.String(length=30), nullable=False, server_default='New'),
        sa.Column('assigned_to_user_id', sa.Integer(), nullable=True),
        sa.Column('created_by_user_id', sa.Integer(), nullable=True),
        sa.Column('sensor_event_id', sa.Integer(), nullable=True),
        sa.Column('sla_deadline', sa.DateTime(), nullable=False),
        sa.Column('resolution_notes', sa.String(length=1000), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['facility_id'], ['facilities.id'], ),
        sa.ForeignKeyConstraint(['assigned_to_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maintenance_tickets_id'), 'maintenance_tickets', ['id'], unique=False)
    op.create_index(op.f('ix_maintenance_tickets_ticket_number'), 'maintenance_tickets', ['ticket_number'], unique=True)

    # Sensor Events table
    op.create_table(
        'sensor_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.String(length=100), nullable=False),
        sa.Column('sensor_id', sa.String(length=50), nullable=False),
        sa.Column('sensor_type', sa.String(length=30), nullable=False),
        sa.Column('facility_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('threshold', sa.Float(), nullable=False),
        sa.Column('is_breached', sa.Boolean(), nullable=False),
        sa.Column('processed_at', sa.DateTime(), nullable=False),
        sa.Column('maintenance_ticket_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['facility_id'], ['facilities.id'], ),
        sa.ForeignKeyConstraint(['maintenance_ticket_id'], ['maintenance_tickets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sensor_events_id'), 'sensor_events', ['id'], unique=False)
    op.create_index(op.f('ix_sensor_events_event_id'), 'sensor_events', ['event_id'], unique=True)

    # Audit Logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('old_state', sa.String(length=50), nullable=True),
        sa.Column('new_state', sa.String(length=50), nullable=True),
        sa.Column('actor_id', sa.Integer(), nullable=True),
        sa.Column('actor_role', sa.String(length=50), nullable=True),
        sa.Column('details', sa.String(length=1000), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['actor_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)
    op.create_index(op.f('ix_audit_logs_entity_id'), 'audit_logs', ['entity_id'], unique=False)

    # Outbox Events table
    op.create_table(
        'outbox_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('aggregate_type', sa.String(length=50), nullable=False),
        sa.Column('aggregate_id', sa.Integer(), nullable=False),
        sa.Column('payload', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='PENDING'),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('max_retries', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('last_attempt_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_outbox_events_id'), 'outbox_events', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('outbox_events')
    op.drop_table('audit_logs')
    op.drop_table('sensor_events')
    op.drop_table('maintenance_tickets')
    op.drop_table('bookings')
    op.drop_table('facilities')
    op.drop_table('users')
