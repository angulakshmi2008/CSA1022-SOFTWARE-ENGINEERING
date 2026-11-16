-- =========================================================================
-- FulfillIQ Omnichannel Order Fulfilment Architecture
-- PostgreSQL 16 Production Relational Schema
-- Aligned with CO2, BTL-5 Evaluate & BTL-6 Create
-- =========================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table (Core Identity)
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    region_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Versioned Regional Policies (12 Operating Regions)
CREATE TABLE IF NOT EXISTS regional_policies (
    region_id VARCHAR(50) NOT NULL,
    region_name VARCHAR(100) NOT NULL,
    policy_version INTEGER NOT NULL DEFAULT 1,
    tax_rate NUMERIC(6, 4) NOT NULL,
    shipping_fee NUMERIC(10, 2) NOT NULL,
    refund_approval_threshold NUMERIC(10, 2) NOT NULL,
    effective_from TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (region_id, policy_version)
);

-- 3. Products Catalogue Table
CREATE TABLE IF NOT EXISTS products (
    sku VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    base_price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Stock Items Table (with non-negative check constraint)
CREATE TABLE IF NOT EXISTS stock_items (
    sku VARCHAR(100) NOT NULL REFERENCES products(sku),
    region_id VARCHAR(50) NOT NULL,
    on_hand INTEGER NOT NULL DEFAULT 0,
    reserved INTEGER NOT NULL DEFAULT 0,
    version INTEGER NOT NULL DEFAULT 1,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (sku, region_id),
    CONSTRAINT chk_stock_non_negative CHECK ((on_hand - reserved) >= 0)
);

-- 5. Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES users(user_id),
    state VARCHAR(50) NOT NULL,
    region_id VARCHAR(50) NOT NULL,
    policy_version INTEGER NOT NULL,
    subtotal NUMERIC(10, 2) NOT NULL,
    tax_amount NUMERIC(10, 2) NOT NULL,
    shipping_fee NUMERIC(10, 2) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    dispatch_due_at TIMESTAMP WITH TIME ZONE,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Order Lines Table
CREATE TABLE IF NOT EXISTS order_lines (
    line_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    sku VARCHAR(100) NOT NULL REFERENCES products(sku),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL,
    tax_rate NUMERIC(6, 4) NOT NULL,
    tax_amount NUMERIC(10, 2) NOT NULL,
    line_total NUMERIC(10, 2) NOT NULL
);

-- 7. Reservations Table (15-Minute Leases)
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    sku VARCHAR(100) NOT NULL REFERENCES products(sku),
    region_id VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Payment Events Table (Unique Gateway Event Identity)
CREATE TABLE IF NOT EXISTS payment_events (
    event_pk UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    gateway_id VARCHAR(100) NOT NULL,
    event_id VARCHAR(100) NOT NULL,
    order_id UUID NOT NULL REFERENCES orders(order_id),
    amount NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    status VARCHAR(50) NOT NULL,
    signature VARCHAR(255) NOT NULL,
    verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_gateway_event UNIQUE (gateway_id, event_id)
);

-- 9. Refund Requests Table (Dual-Control Governance)
CREATE TABLE IF NOT EXISTS refund_requests (
    refund_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(order_id),
    amount NUMERIC(10, 2) NOT NULL,
    state VARCHAR(50) NOT NULL,
    reason TEXT NOT NULL,
    requested_by UUID NOT NULL REFERENCES users(user_id),
    approved_by UUID REFERENCES users(user_id),
    idempotency_key VARCHAR(100) UNIQUE NOT NULL,
    failure_reason TEXT,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- 10. Transactional Outbox Intents Table
CREATE TABLE IF NOT EXISTS outbox_intents (
    intent_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    aggregate_id UUID NOT NULL,
    purpose VARCHAR(50) NOT NULL,
    correlation_key VARCHAR(100) UNIQUE NOT NULL,
    payload_json JSONB NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 5,
    next_retry_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    external_reference VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. Edge Scanner Event Logs Table (Unique Node/Event Identity)
CREATE TABLE IF NOT EXISTS scanner_event_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id VARCHAR(100) NOT NULL,
    event_id VARCHAR(100) NOT NULL,
    sku VARCHAR(100) NOT NULL REFERENCES products(sku),
    region_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    observation_time TIMESTAMP WITH TIME ZONE NOT NULL,
    received_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    schema_version VARCHAR(20) NOT NULL,
    is_stale BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT uq_scanner_node_event UNIQUE (node_id, event_id)
);

-- 12. Append-Only Audit Trail Table
CREATE TABLE IF NOT EXISTS audit_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor_id VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(100) NOT NULL,
    old_version INTEGER,
    new_version INTEGER,
    details_json JSONB,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_orders_owner ON orders(owner_id);
CREATE INDEX IF NOT EXISTS idx_orders_state ON orders(state);
CREATE INDEX IF NOT EXISTS idx_outbox_pending ON outbox_intents(status, next_retry_at);
CREATE INDEX IF NOT EXISTS idx_reservations_expiry ON reservations(status, expires_at);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_events(entity_type, entity_id);
