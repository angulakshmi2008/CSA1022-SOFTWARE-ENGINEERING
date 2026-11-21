<template>
  <div class="min-h-screen flex flex-col">
    <!-- Top Header -->
    <header class="top-header">
      <div class="brand-title">
        <span>🏛️</span>
        <span>Smart Campus Facility Booking & Maintenance Platform</span>
      </div>
      <div style="display: flex; align-items: center; gap: 1rem;">
        <span style="font-size: 0.85rem; color: #94a3b8;">
          Instance: <strong style="color: #38bdf8;">{{ healthInfo.instance_id || 'backend-1' }}</strong> | DB: <span style="color: #4ade80;">{{ healthInfo.database || 'healthy' }}</span>
        </span>
        <div style="background: #1e293b; padding: 0.35rem 0.75rem; border-radius: 0.375rem; font-size: 0.85rem;">
          👤 <strong>{{ currentUser ? currentUser.username : 'Not Signed In' }}</strong>
          <span style="color: #38bdf8; margin-left: 0.35rem;">({{ currentUser ? currentUser.role_display : '' }})</span>
        </div>
      </div>
    </header>

    <!-- Interactive Demonstration Persona Switcher -->
    <div class="role-bar">
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <strong style="color: #f8fafc; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">Role Persona (Demonstration):</strong>
        <div class="role-pills">
          <button
            v-for="p in personas"
            :key="p.username"
            class="role-pill"
            :class="{ active: currentUser && currentUser.username === p.username }"
            @click="switchPersona(p)"
          >
            {{ p.label }} [{{ p.role }}]
          </button>
        </div>
      </div>
      <div>
        <span style="font-size: 0.75rem; color: #94a3b8;">*Server strictly validates permissions per API call</span>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <nav class="nav-tabs">
      <button class="nav-tab" :class="{ active: activeTab === 'dashboard' }" @click="activeTab = 'dashboard'">
        📊 Dashboard & SLAs
      </button>
      <button class="nav-tab" :class="{ active: activeTab === 'facilities' }" @click="activeTab = 'facilities'">
        🏢 Facilities & Booking Calendar
      </button>
      <button class="nav-tab" :class="{ active: activeTab === 'maintenance' }" @click="activeTab = 'maintenance'">
        🛠️ Maintenance & Triage Queue
      </button>
      <button class="nav-tab" :class="{ active: activeTab === 'sensor' }" @click="activeTab = 'sensor'">
        📡 Sensor Telemetry Intake
      </button>
      <button class="nav-tab" :class="{ active: activeTab === 'approvals' }" @click="activeTab = 'approvals'">
        ✅ Approvals
        <span v-if="pendingApprovalsCount > 0" style="background: #ef4444; color: #fff; border-radius: 9999px; padding: 0.1rem 0.45rem; font-size: 0.7rem; font-weight: 700; margin-left: 0.25rem;">
          {{ pendingApprovalsCount }}
        </span>
      </button>
      <button class="nav-tab" :class="{ active: activeTab === 'loans' }" @click="activeTab = 'loans'">
        📦 Equipment Loans
      </button>
      <button class="nav-tab" :class="{ active: activeTab === 'integrations' }" @click="activeTab = 'integrations'">
        🔗 DevOps & External Issues
      </button>
      <button class="nav-tab" :class="{ active: activeTab === 'audit' }" @click="activeTab = 'audit'">
        📜 Transactional Audit Trail
      </button>
    </nav>

    <!-- Global Alert / Status Banner -->
    <div v-if="globalNotification" class="container" style="padding-bottom: 0;">
      <div :class="['alert', 'alert-' + globalNotification.type]">
        <span>{{ globalNotification.icon }}</span>
        <span>{{ globalNotification.text }}</span>
        <button @click="globalNotification = null" style="margin-left: auto; background: none; border: none; cursor: pointer; font-weight: bold;">✕</button>
      </div>
    </div>

    <!-- Tab Views -->
    <main class="container">
      <!-- 1. Operations Dashboard -->
      <section v-if="activeTab === 'dashboard'">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Campus Operations & SLA Metrics</h2>
            <div>
              <label style="font-size: 0.85rem; font-weight: 500; margin-right: 0.5rem;">Campus Filter:</label>
              <select v-model="selectedCampus" @change="loadDashboard" class="form-select" style="width: auto; display: inline-block;">
                <option value="">All Campuses (6 Total)</option>
                <option v-for="c in campuses" :key="c.id" :value="c.id">{{ c.name }} ({{ c.code }})</option>
              </select>
              <button class="btn btn-outline btn-sm" @click="loadDashboard" style="margin-left: 0.5rem;">🔄 Refresh</button>
            </div>
          </div>

          <!-- KPI Cards -->
          <div class="kpi-grid">
            <div class="kpi-card">
              <span class="kpi-label">Active Facility Bookings</span>
              <span class="kpi-val" style="color: #2563eb;">{{ summary.metrics.active_bookings }}</span>
              <span class="kpi-sub">Approved / Confirmed / In-Use</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Open Maintenance Tickets</span>
              <span class="kpi-val" style="color: #d97706;">{{ summary.metrics.open_tickets }}</span>
              <span class="kpi-sub">Awaiting closure / In Progress</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Pending Governance Approvals</span>
              <span class="kpi-val" style="color: #7c3aed;">{{ summary.metrics.pending_approvals }}</span>
              <span class="kpi-sub">Restricted labs & equipment</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">SLA Target Risk (&lt; 1h)</span>
              <span class="kpi-val" :style="{ color: summary.metrics.sla_at_risk > 0 ? '#dc2626' : '#16a34a' }">
                {{ summary.metrics.sla_at_risk }}
              </span>
              <span class="kpi-sub">Critical or near-deadline work</span>
            </div>
          </div>

          <!-- Priority Matrix Breakdown -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="border: 1px solid var(--border); border-radius: 0.5rem; padding: 1rem; background: #fff;">
              <h3 style="font-size: 0.95rem; font-weight: 600; margin-bottom: 0.75rem;">Active Tickets by Priority Matrix</h3>
              <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                <div style="flex: 1; padding: 0.75rem; background: #fee2e2; border-radius: 0.375rem; text-align: center;">
                  <div style="font-weight: 700; color: #991b1b; font-size: 1.25rem;">{{ summary.priority_breakdown.M1 || 0 }}</div>
                  <div style="font-size: 0.75rem; color: #991b1b; font-weight: 600;">M1 Critical (2h)</div>
                </div>
                <div style="flex: 1; padding: 0.75rem; background: #ffedd5; border-radius: 0.375rem; text-align: center;">
                  <div style="font-weight: 700; color: #9a3412; font-size: 1.25rem;">{{ summary.priority_breakdown.M2 || 0 }}</div>
                  <div style="font-size: 0.75rem; color: #9a3412; font-weight: 600;">M2 High (4h)</div>
                </div>
                <div style="flex: 1; padding: 0.75rem; background: #fef9c3; border-radius: 0.375rem; text-align: center;">
                  <div style="font-weight: 700; color: #854d0e; font-size: 1.25rem;">{{ summary.priority_breakdown.M3 || 0 }}</div>
                  <div style="font-size: 0.75rem; color: #854d0e; font-weight: 600;">M3 Medium (8h)</div>
                </div>
                <div style="flex: 1; padding: 0.75rem; background: #ecfdf5; border-radius: 0.375rem; text-align: center;">
                  <div style="font-weight: 700; color: #065f46; font-size: 1.25rem;">{{ summary.priority_breakdown.M4 || 0 }}</div>
                  <div style="font-size: 0.75rem; color: #065f46; font-weight: 600;">M4 Low (24h)</div>
                </div>
              </div>
            </div>

            <div style="border: 1px solid var(--border); border-radius: 0.5rem; padding: 1rem; background: #fff;">
              <h3 style="font-size: 0.95rem; font-weight: 600; margin-bottom: 0.75rem;">Six-Campus Network Infrastructure</h3>
              <ul style="font-size: 0.85rem; list-style: none;">
                <li v-for="c in campuses" :key="c.code" style="padding: 0.3rem 0; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between;">
                  <span>🏛️ {{ c.name }} ({{ c.code }})</span>
                  <span style="color: var(--text-muted);">{{ c.city }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- 2. Facility Catalogue & Booking Calendar -->
      <section v-if="activeTab === 'facilities'">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Campus Facilities Catalogue & Availability</h2>
            <button class="btn btn-primary" @click="openBookingModal(null)">
              ➕ New Facility Booking Request
            </button>
          </div>

          <!-- Facilities Table -->
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Campus</th>
                  <th>Facility Name</th>
                  <th>Code</th>
                  <th>Type</th>
                  <th>Capacity</th>
                  <th>Governance</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="f in facilities" :key="f.id">
                  <td><strong>{{ f.campus_code }}</strong></td>
                  <td>{{ f.name }}</td>
                  <td><code>{{ f.code }}</code></td>
                  <td>{{ f.facility_type_display }}</td>
                  <td>{{ f.capacity }} seats</td>
                  <td>
                    <span v-if="f.is_restricted" class="badge" style="background: #fef2f2; color: #b91c1c; border: 1px solid #f87171;">
                      🔒 Restricted (Approver Required)
                    </span>
                    <span v-else class="badge" style="background: #f0fdf4; color: #15803d; border: 1px solid #86efac;">
                      ✅ Open Booking
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-outline btn-sm" @click="viewCalendarForFacility(f)">
                      📅 View Schedule
                    </button>
                    <button class="btn btn-primary btn-sm" @click="openBookingModal(f)" style="margin-left: 0.35rem;">
                      Book Slot
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Selected Facility Calendar Display -->
        <div v-if="selectedFacilityForCalendar" class="card">
          <div class="card-header">
            <h3 class="card-title">Schedule for {{ selectedFacilityForCalendar.name }} ({{ selectedFacilityForCalendar.code }})</h3>
            <button class="btn btn-outline btn-sm" @click="selectedFacilityForCalendar = null">Close Schedule</button>
          </div>
          <div v-if="facilityCalendarBookings.length === 0" style="padding: 1.5rem; text-align: center; color: var(--text-muted);">
            No reservations scheduled for this facility. Space is 100% available!
          </div>
          <div v-else class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Booking ID</th>
                  <th>Reserved Time Interval (UTC)</th>
                  <th>Status</th>
                  <th>Purpose</th>
                  <th>Reserved By</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="b in facilityCalendarBookings" :key="b.id">
                  <td>#{{ b.id }}</td>
                  <td>
                    <strong>{{ formatTime(b.start_at) }}</strong> to <strong>{{ formatTime(b.end_at) }}</strong>
                  </td>
                  <td>
                    <span :class="['badge', 'badge-' + b.status]">{{ b.status }}</span>
                  </td>
                  <td>{{ b.purpose }}</td>
                  <td>{{ b.requester_name }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- 3. Maintenance Queue & Explainable Triage -->
      <section v-if="activeTab === 'maintenance'">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Maintenance Workorder Queue & Explainable Triage</h2>
            <button class="btn btn-primary" @click="showNewTicketModal = true">
              ➕ Report Maintenance Issue
            </button>
          </div>

          <!-- Filter Bar -->
          <div style="display: flex; gap: 0.75rem; margin-bottom: 1rem; flex-wrap: wrap;">
            <select v-model="ticketFilterStatus" @change="loadTickets" class="form-select" style="width: auto;">
              <option value="">All Statuses</option>
              <option value="intake">Intake</option>
              <option value="triaged">Triaged</option>
              <option value="assigned">Assigned</option>
              <option value="in_progress">In Progress</option>
              <option value="inspection">Inspection</option>
              <option value="pending_approval">Pending Approval</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
            <select v-model="ticketFilterPriority" @change="loadTickets" class="form-select" style="width: auto;">
              <option value="">All Priorities</option>
              <option value="M1">M1 - Critical</option>
              <option value="M2">M2 - High</option>
              <option value="M3">M3 - Medium</option>
              <option value="M4">M4 - Low</option>
            </select>
          </div>

          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Ticket</th>
                  <th>Priority</th>
                  <th>Category</th>
                  <th>Status</th>
                  <th>Assignee</th>
                  <th>SLA Deadline</th>
                  <th>Triage Logic</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="t in tickets" :key="t.id">
                  <td>
                    <strong>#{{ t.id }}</strong>: {{ t.title }}
                    <div style="font-size: 0.75rem; color: var(--text-muted);">
                      {{ t.campus_name }} | {{ t.source }}
                    </div>
                  </td>
                  <td>
                    <span :class="['badge', 'badge-' + t.priority.toLowerCase()]">{{ t.priority }}</span>
                  </td>
                  <td>{{ t.category_display }}</td>
                  <td>
                    <span class="badge" style="background: #e2e8f0; color: #1e293b;">{{ t.status }}</span>
                    <span v-if="t.is_restricted_change" style="display: block; font-size: 0.7rem; color: #b91c1c;">⚠️ Change Review</span>
                  </td>
                  <td>{{ t.assignee_name || 'Unassigned' }}</td>
                  <td>
                    <span v-if="t.sla_due_at" :style="{ color: t.is_sla_breached ? '#dc2626' : '#334155', fontWeight: t.is_sla_breached ? '700' : 'normal' }">
                      {{ formatTime(t.sla_due_at) }}
                      <span v-if="t.is_sla_breached" style="font-size: 0.7rem; display: block; color: #dc2626;">🚨 SLA BREACHED</span>
                    </span>
                    <span v-else>—</span>
                  </td>
                  <td>
                    <button class="btn btn-outline btn-sm" @click="viewTriageExplanation(t)">
                      💡 View Rationale
                    </button>
                  </td>
                  <td>
                    <button class="btn btn-primary btn-sm" @click="openTicketActionModal(t)">
                      Inspect / Update
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- 4. Sensor Telemetry Intake Simulator -->
      <section v-if="activeTab === 'sensor'">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Controlled IoT Sensor Telemetry Intake Simulator</h2>
          </div>
          <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1.5rem;">
            Simulate automated telemetry emissions from campus environmental and mechanical sensors.
            Tests threshold breach ticket creation, priority calculation, and deduplication of repeated events.
          </p>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem;">
            <!-- Simulation Form -->
            <div style="border: 1px solid var(--border); border-radius: 0.5rem; padding: 1.25rem; background: #fff;">
              <h3 style="font-size: 1rem; font-weight: 600; margin-bottom: 1rem;">Telemetry Generator</h3>
              
              <div class="form-group">
                <label class="form-label">Sensor Hardware Source ID:</label>
                <input v-model="sensorSim.source_id" class="form-input" />
              </div>
              
              <div class="form-group">
                <label class="form-label">Unique Event Identity (UUID):</label>
                <div style="display: flex; gap: 0.5rem;">
                  <input v-model="sensorSim.event_id" class="form-input" />
                  <button class="btn btn-outline btn-sm" @click="regenerateEventId">🎲 New UUID</button>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Telemetry Metric:</label>
                <select v-model="sensorSim.metric" class="form-select">
                  <option value="temperature_celsius">temperature_celsius (Threshold > 26.0°C)</option>
                  <option value="vibration_hz">vibration_hz (Threshold > 45.0 Hz)</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Telemetry Value: <strong>{{ sensorSim.value }}</strong></label>
                <input type="range" v-model.number="sensorSim.value" min="15" max="45" step="0.5" style="width: 100%;" />
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted);">
                  <span>15 (Normal)</span>
                  <span style="color: #ea580c; font-weight: 600;">26.0 (Warning)</span>
                  <span style="color: #dc2626; font-weight: 700;">30+ (Critical M1)</span>
                </div>
              </div>

              <div style="display: flex; gap: 0.75rem; margin-top: 1.5rem;">
                <button class="btn btn-primary" @click="sendSensorTelemetry(false)">
                  📡 Dispatch Telemetry Event
                </button>
                <button class="btn btn-outline" @click="sendSensorTelemetry(true)" title="Sends the exact same source_id + event_id again to prove duplicate suppression">
                  🔁 Simulate Retry (Repeat Event)
                </button>
              </div>
            </div>

            <!-- Ingestion Result Box -->
            <div style="border: 1px solid var(--border); border-radius: 0.5rem; padding: 1.25rem; background: #fff;">
              <h3 style="font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem;">Ingestion & Deduplication Response</h3>
              <div v-if="sensorResult" class="code-box">
                <pre>{{ JSON.stringify(sensorResult, null, 2) }}</pre>
              </div>
              <div v-else style="padding: 2rem; text-align: center; color: var(--text-muted);">
                Dispatch an event to inspect server response and deduplication behavior.
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 5. Approval Centre -->
      <section v-if="activeTab === 'approvals'">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Governance & Approvals Centre</h2>
            <span style="font-size: 0.85rem; color: var(--text-muted);">
              Current Persona: <strong>{{ currentUser ? currentUser.role_display : '' }}</strong>
            </span>
          </div>

          <div v-if="pendingApprovals.length === 0" style="padding: 2rem; text-align: center; color: var(--text-muted);">
            No items currently pending approval. All facility bookings and hardware changes are settled!
          </div>

          <div v-else class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Request Type</th>
                  <th>Resource / Operation</th>
                  <th>Requester</th>
                  <th>Interval / Purpose</th>
                  <th>Submitted At</th>
                  <th>Decision Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in pendingApprovals" :key="item.type + '-' + item.id">
                  <td>
                    <span class="badge" style="background: #ede9fe; color: #5b21b6;">{{ item.type }}</span>
                  </td>
                  <td><strong>{{ item.title }}</strong></td>
                  <td>{{ item.requester }}</td>
                  <td>{{ item.purpose }}</td>
                  <td>{{ formatTime(item.created_at) }}</td>
                  <td>
                    <button class="btn btn-success btn-sm" @click="openApprovalDialog(item, 'approved')">
                      ✓ Approve
                    </button>
                    <button class="btn btn-danger btn-sm" @click="openApprovalDialog(item, 'rejected')" style="margin-left: 0.35rem;">
                      ✕ Reject
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- 6. Equipment Loans -->
      <section v-if="activeTab === 'loans'">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Asset & Equipment Loan Requests</h2>
            <button class="btn btn-primary" @click="showNewLoanModal = true">
              ➕ Request Equipment Loan
            </button>
          </div>

          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Loan ID</th>
                  <th>Asset Name</th>
                  <th>Asset Code</th>
                  <th>Requester</th>
                  <th>Duration</th>
                  <th>Status</th>
                  <th>Purpose</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="l in loans" :key="l.id">
                  <td>#{{ l.id }}</td>
                  <td><strong>{{ l.asset_name }}</strong></td>
                  <td><code>{{ l.asset_code }}</code></td>
                  <td>{{ l.requester_name }}</td>
                  <td>{{ formatTime(l.start_at) }} to {{ formatTime(l.end_at) }}</td>
                  <td>
                    <span class="badge" :class="l.status === 'approved' ? 'badge-confirmed' : 'badge-requested'">{{ l.status }}</span>
                  </td>
                  <td>{{ l.purpose }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- 7. DevOps & Integration Status -->
      <section v-if="activeTab === 'integrations'">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">DevOps & Issue Tracker Integration (Durable Outbox)</h2>
            <button class="btn btn-primary" @click="showNewIntentModal = true">
              ➕ Enqueue Developer Issue
            </button>
          </div>
          <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1rem;">
            Durable integration intents track outward operations to developer issue trackers (e.g. Jira / GitHub Issues).
            Guarantees idempotent reconciliation across network timeouts using stable correlation keys.
          </p>

          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Intent ID</th>
                  <th>Linked Ticket</th>
                  <th>Correlation Key</th>
                  <th>External Issue ID</th>
                  <th>Attempts</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="int in intents" :key="int.id">
                  <td>#{{ int.id }}</td>
                  <td>#{{ int.ticket }}: {{ int.ticket_title }}</td>
                  <td><code>{{ int.correlation_key }}</code></td>
                  <td>
                    <span v-if="int.external_id" style="font-weight: 600; color: #2563eb;">{{ int.external_id }}</span>
                    <span v-else style="color: var(--text-muted);">None</span>
                  </td>
                  <td>{{ int.attempts }}</td>
                  <td>
                    <span class="badge" style="background: #ecfdf5; color: #065f46;">{{ int.status }}</span>
                  </td>
                  <td>
                    <button class="btn btn-outline btn-sm" @click="retryIntegration(int.id)">
                      🔄 Reconcile / Retry
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- 8. Transactional Audit Log -->
      <section v-if="activeTab === 'audit'">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Immutable Transactional Audit Trail</h2>
            <button class="btn btn-outline btn-sm" @click="loadAudits">🔄 Refresh Log</button>
          </div>
          <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1rem;">
            Append-only records capturing all state mutations, security-sensitive approvals, and concurrency events.
          </p>

          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Actor</th>
                  <th>Role</th>
                  <th>Target Entity</th>
                  <th>Action</th>
                  <th>State Delta / Changes</th>
                  <th>Client IP</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="a in audits" :key="a.id">
                  <td><code style="font-size: 0.75rem;">{{ formatTime(a.created_at) }}</code></td>
                  <td><strong>{{ a.actor_username || 'System' }}</strong></td>
                  <td><span class="badge" style="background: #f1f5f9; color: #475569;">{{ a.actor_role || 'System' }}</span></td>
                  <td>{{ a.entity_type }} #{{ a.entity_id }}</td>
                  <td><strong>{{ a.action }}</strong></td>
                  <td>
                    <div style="font-size: 0.75rem; max-width: 400px; max-height: 80px; overflow-y: auto;">
                      <pre style="white-space: pre-wrap; font-family: 'JetBrains Mono', monospace;">{{ JSON.stringify(a.after_state, null, 1) }}</pre>
                    </div>
                  </td>
                  <td><code style="font-size: 0.75rem;">{{ a.ip_address || '127.0.0.1' }}</code></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>

    <!-- Modal: New Booking -->
    <div v-if="showBookingModal" class="modal-overlay">
      <div class="modal-card">
        <h3 class="card-title" style="margin-bottom: 1rem;">Create Facility Reservation</h3>

        <div v-if="bookingError" class="alert alert-error">
          <span>⚠️</span>
          <span>{{ bookingError }}</span>
        </div>

        <form @submit.prevent="submitBooking">
          <div class="form-group">
            <label class="form-label">Facility:</label>
            <select v-model="bookingForm.facility" class="form-select" required>
              <option v-for="f in facilities" :key="f.id" :value="f.id">
                {{ f.campus_code }} - {{ f.name }} ({{ f.code }}) {{ f.is_restricted ? '[Restricted]' : '' }}
              </option>
            </select>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div class="form-group">
              <label class="form-label">Start Time (UTC):</label>
              <input type="datetime-local" v-model="bookingForm.start_at" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">End Time (UTC):</label>
              <input type="datetime-local" v-model="bookingForm.end_at" class="form-input" required />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Purpose / Academic Activity:</label>
            <textarea v-model="bookingForm.purpose" class="form-textarea" rows="3" required></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">Client Idempotency Key:</label>
            <input v-model="bookingForm.request_key" class="form-input" />
            <span style="font-size: 0.75rem; color: var(--text-muted);">Prevents duplicate bookings on network retries.</span>
          </div>

          <div style="display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem;">
            <button type="button" class="btn btn-outline" @click="showBookingModal = false">Cancel</button>
            <button type="submit" class="btn btn-primary">Confirm Reservation</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal: Ticket Action / Inspection / Resolution -->
    <div v-if="selectedTicketForAction" class="modal-overlay">
      <div class="modal-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <h3 class="card-title">Manage Ticket #{{ selectedTicketForAction.id }}</h3>
          <span :class="['badge', 'badge-' + selectedTicketForAction.priority.toLowerCase()]">
            {{ selectedTicketForAction.priority }}
          </span>
        </div>

        <div v-if="ticketActionError" class="alert alert-error">
          <span>⚠️</span>
          <span>{{ ticketActionError }}</span>
        </div>

        <div style="background: #f8fafc; padding: 1rem; border-radius: 0.375rem; margin-bottom: 1rem; font-size: 0.85rem;">
          <div><strong>Title:</strong> {{ selectedTicketForAction.title }}</div>
          <div><strong>Current Status:</strong> <span class="badge" style="background:#e2e8f0; color:#1e293b;">{{ selectedTicketForAction.status }}</span></div>
          <div><strong>Current Version:</strong> v{{ selectedTicketForAction.version }} (Used for Optimistic Concurrency Check)</div>
          <div><strong>Assignee:</strong> {{ selectedTicketForAction.assignee_name || 'Unassigned' }}</div>
        </div>

        <!-- Assign Technician Section -->
        <div v-if="currentUser && (currentUser.role === 'facility_manager' || currentUser.role === 'administrator')" style="margin-bottom: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem;">
          <label class="form-label">Assign Maintenance Technician:</label>
          <div style="display: flex; gap: 0.5rem;">
            <select v-model="assignTechnicianId" class="form-select">
              <option value="">Select Technician...</option>
              <option v-for="tech in technicians" :key="tech.id" :value="tech.id">
                {{ tech.first_name }} {{ tech.last_name }} ({{ tech.username }}) - {{ tech.department }}
              </option>
            </select>
            <button class="btn btn-primary" @click="assignSelectedTechnician">Assign</button>
          </div>
        </div>

        <!-- Add Inspection Note -->
        <div style="margin-bottom: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem;">
          <label class="form-label">Add Inspection / Diagnostic Finding:</label>
          <textarea v-model="newInspectionNote" class="form-textarea" rows="2" placeholder="Record diagnostic notes, measured values, or photos..."></textarea>
          <button class="btn btn-outline btn-sm" @click="submitInspectionNote" style="margin-top: 0.5rem;">
            📝 Log Inspection Note
          </button>
        </div>

        <!-- Lifecycle Transition Section -->
        <div>
          <label class="form-label">Transition State (FSM):</label>
          <div class="form-group">
            <select v-model="targetTicketState" class="form-select">
              <option value="in_progress">In Progress</option>
              <option value="inspection">Inspection</option>
              <option value="pending_approval">Pending Approval (Restricted Change)</option>
              <option value="resolved">Resolved (Requires Resolution Notes)</option>
              <option value="closed">Closed (Manager Verification)</option>
            </select>
          </div>

          <div class="form-group" v-if="targetTicketState === 'resolved' || targetTicketState === 'closed'">
            <label class="form-label">
              Resolution Notes & Verification Evidence <strong style="color: #dc2626;">*MANDATORY (HTTP 422 if missing)</strong>:
            </label>
            <textarea v-model="resolutionNotesInput" class="form-textarea" rows="3" placeholder="Describe corrective maintenance actions, parts replaced, and verification test outcome..."></textarea>
          </div>

          <div style="display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1rem;">
            <button type="button" class="btn btn-outline" @click="selectedTicketForAction = null">Close</button>
            <button type="button" class="btn btn-primary" @click="executeTicketTransition">Apply Transition</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal: Approval Justification Dialog -->
    <div v-if="approvalDialogItem" class="modal-overlay">
      <div class="modal-card">
        <h3 class="card-title">Record Approval Decision</h3>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
          {{ approvalDialogDecision === 'approved' ? 'Approving' : 'Rejecting' }} <strong>{{ approvalDialogItem.title }}</strong>
        </p>

        <div v-if="approvalError" class="alert alert-error">
          <span>⚠️</span>
          <span>{{ approvalError }}</span>
        </div>

        <div class="form-group">
          <label class="form-label">Auditable Justification Reason (Required):</label>
          <textarea v-model="approvalReason" class="form-textarea" rows="3" required placeholder="Enter formal departmental justification or safety risk assessment..."></textarea>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1rem;">
          <button class="btn btn-outline" @click="approvalDialogItem = null">Cancel</button>
          <button :class="['btn', approvalDialogDecision === 'approved' ? 'btn-success' : 'btn-danger']" @click="submitApprovalDecision">
            Confirm {{ approvalDialogDecision }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal: Explainable Triage View -->
    <div v-if="activeTriageExplanation" class="modal-overlay">
      <div class="modal-card">
        <h3 class="card-title">Explainable Triage Recommendation</h3>
        <div class="code-box" style="white-space: pre-wrap; font-size: 0.85rem; padding: 1rem;">
          {{ activeTriageExplanation }}
        </div>
        <div style="display: flex; justify-content: flex-end; margin-top: 1rem;">
          <button class="btn btn-primary" @click="activeTriageExplanation = null">Dismiss</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { api, setAuthSession, getCurrentUser } from './api.js';

export default {
  data() {
    return {
      activeTab: 'dashboard',
      healthInfo: {},
      currentUser: null,
      selectedCampus: '',
      campuses: [],
      facilities: [],
      tickets: [],
      technicians: [],
      audits: [],
      intents: [],
      loans: [],
      pendingApprovals: [],
      pendingApprovalsCount: 0,

      // Summary
      summary: {
        metrics: { active_bookings: 0, open_tickets: 0, pending_approvals: 0, sla_at_risk: 0, total_facilities: 0 },
        priority_breakdown: {}
      },

      // Personas for instant switching
      personas: [
        { label: 'Admin', username: 'admin', role: 'administrator' },
        { label: 'Approver (Dr. Kumar)', username: 'approver.dr.kumar', role: 'department_approver' },
        { label: 'Manager (Priya)', username: 'manager.priya', role: 'facility_manager' },
        { label: 'Technician (Rajesh)', username: 'tech.rajesh', role: 'technician' },
        { label: 'Faculty (Dr. Anand)', username: 'faculty.dr.anand', role: 'faculty' },
        { label: 'Student (Arun)', username: 'student.arun', role: 'student' },
      ],

      // Calendar
      selectedFacilityForCalendar: null,
      facilityCalendarBookings: [],

      // Booking modal
      showBookingModal: false,
      bookingError: null,
      bookingForm: {
        facility: null,
        start_at: '',
        end_at: '',
        purpose: '',
        request_key: ''
      },

      // Ticket Action modal
      selectedTicketForAction: null,
      ticketActionError: null,
      assignTechnicianId: '',
      newInspectionNote: '',
      targetTicketState: 'in_progress',
      resolutionNotesInput: '',
      activeTriageExplanation: null,
      showNewTicketModal: false,

      // Sensor Simulation
      sensorSim: {
        source_id: 'HVAC-TEMP-UNIT-04',
        event_id: 'evt-sim-' + Math.floor(Math.random() * 100000),
        metric: 'temperature_celsius',
        value: 29.5
      },
      sensorResult: null,

      // Approval Dialog
      approvalDialogItem: null,
      approvalDialogDecision: 'approved',
      approvalReason: '',
      approvalError: null,

      // Global Alert
      globalNotification: null
    };
  },
  async mounted() {
    await this.checkHealth();
    await this.initDefaultPersona();
    await this.loadInitialData();
  },
  methods: {
    async checkHealth() {
      try {
        this.healthInfo = await api.getHealth();
      } catch (e) {
        this.healthInfo = { status: 'unhealthy', database: 'disconnected', instance_id: 'backend-offline' };
      }
    },
    async initDefaultPersona() {
      const stored = getCurrentUser();
      if (stored) {
        this.currentUser = stored;
      } else {
        await this.switchPersona(this.personas[0]); // default admin
      }
    },
    async switchPersona(p) {
      try {
        const res = await api.login(p.username, 'Password@123');
        setAuthSession(res.token, res.user);
        this.currentUser = res.user;
        this.showNotification('info', `Switched active persona to ${p.label} (${res.user.role})`);
        await this.loadInitialData();
      } catch (err) {
        console.error("Failed to switch persona:", err);
      }
    },
    showNotification(type, text) {
      const icons = { success: '✅', error: '⚠️', info: 'ℹ️', warning: '⚡' };
      this.globalNotification = { type, text, icon: icons[type] || 'ℹ️' };
      setTimeout(() => {
        if (this.globalNotification && this.globalNotification.text === text) {
          this.globalNotification = null;
        }
      }, 5000);
    },
    async loadInitialData() {
      await Promise.all([
        this.loadDashboard(),
        this.loadCampuses(),
        this.loadFacilities(),
        this.loadTickets(),
        this.loadPendingApprovals(),
        this.loadAudits(),
        this.loadIntents(),
        this.loadLoans(),
        this.loadTechnicians()
      ]);
    },
    async loadDashboard() {
      try {
        this.summary = await api.getDashboardSummary(this.selectedCampus);
      } catch (e) {
        console.error(e);
      }
    },
    async loadCampuses() {
      try {
        this.campuses = await api.getCampuses();
      } catch (e) {
        console.error(e);
      }
    },
    async loadFacilities() {
      try {
        this.facilities = await api.getFacilities();
      } catch (e) {
        console.error(e);
      }
    },
    async loadTickets() {
      try {
        let params = [];
        if (this.ticketFilterStatus) params.push(`status=${this.ticketFilterStatus}`);
        if (this.ticketFilterPriority) params.push(`priority=${this.ticketFilterPriority}`);
        this.tickets = await api.getTickets(params.join('&'));
      } catch (e) {
        console.error(e);
      }
    },
    async loadTechnicians() {
      try {
        this.technicians = await api.getUsers('role=technician');
      } catch (e) {
        console.error(e);
      }
    },
    async loadPendingApprovals() {
      try {
        this.pendingApprovals = await api.getPendingApprovals();
        this.pendingApprovalsCount = this.pendingApprovals.length;
      } catch (e) {
        this.pendingApprovals = [];
        this.pendingApprovalsCount = 0;
      }
    },
    async loadAudits() {
      try {
        this.audits = await api.getAuditEvents();
      } catch (e) {
        console.error(e);
      }
    },
    async loadIntents() {
      try {
        this.intents = await api.getIntents();
      } catch (e) {
        console.error(e);
      }
    },
    async loadLoans() {
      try {
        this.loans = await api.getEquipmentLoans();
      } catch (e) {
        console.error(e);
      }
    },
    async viewCalendarForFacility(f) {
      this.selectedFacilityForCalendar = f;
      try {
        this.facilityCalendarBookings = await api.getCalendar(`facility_id=${f.id}`);
      } catch (e) {
        this.facilityCalendarBookings = [];
      }
    },
    openBookingModal(facility) {
      this.bookingError = null;
      const now = new Date();
      now.setHours(now.getHours() + 1, 0, 0, 0);
      const end = new Date(now.getTime() + 2 * 3600 * 1000);

      this.bookingForm = {
        facility: facility ? facility.id : (this.facilities[0] ? this.facilities[0].id : null),
        start_at: now.toISOString().slice(0, 16),
        end_at: end.toISOString().slice(0, 16),
        purpose: 'Advanced Computing Practical Session',
        request_key: 'req-token-' + Math.floor(Math.random() * 1000000)
      };
      this.showBookingModal = true;
    },
    async submitBooking() {
      this.bookingError = null;
      try {
        const payload = {
          facility: this.bookingForm.facility,
          start_at: new Date(this.bookingForm.start_at).toISOString(),
          end_at: new Date(this.bookingForm.end_at).toISOString(),
          purpose: this.bookingForm.purpose,
          request_key: this.bookingForm.request_key
        };
        const res = await api.createBooking(payload);
        this.showBookingModal = false;
        this.showNotification('success', `Booking #${res.id} created successfully! (Status: ${res.status})`);
        await this.loadDashboard();
        if (this.selectedFacilityForCalendar && this.selectedFacilityForCalendar.id === payload.facility) {
          await this.viewCalendarForFacility(this.selectedFacilityForCalendar);
        }
      } catch (err) {
        this.bookingError = err.message || (err.data && err.data.detail) || "Failed to create booking.";
      }
    },
    openTicketActionModal(ticket) {
      this.selectedTicketForAction = ticket;
      this.ticketActionError = null;
      this.targetTicketState = ticket.status === 'intake' ? 'triaged' : (ticket.status === 'triaged' ? 'assigned' : 'in_progress');
      this.resolutionNotesInput = ticket.resolution_notes || '';
      this.assignTechnicianId = ticket.assignee || '';
      this.newInspectionNote = '';
    },
    async assignSelectedTechnician() {
      if (!this.assignTechnicianId) return;
      try {
        const updated = await api.assignTechnician(this.selectedTicketForAction.id, this.assignTechnicianId);
        this.selectedTicketForAction = updated;
        this.showNotification('success', `Assigned technician to Ticket #${updated.id}`);
        await this.loadTickets();
      } catch (err) {
        this.ticketActionError = err.message || "Failed to assign technician.";
      }
    },
    async submitInspectionNote() {
      if (!this.newInspectionNote.trim()) return;
      try {
        await api.addInspection(this.selectedTicketForAction.id, { notes: this.newInspectionNote });
        this.newInspectionNote = '';
        this.showNotification('success', 'Inspection finding logged in work history.');
        await this.loadTickets();
      } catch (err) {
        this.ticketActionError = err.message || "Failed to log inspection note.";
      }
    },
    async executeTicketTransition() {
      this.ticketActionError = null;
      try {
        const payload = {
          target_state: this.targetTicketState,
          expected_version: this.selectedTicketForAction.version,
          resolution_notes: this.resolutionNotesInput
        };
        const updated = await api.updateTicketState(this.selectedTicketForAction.id, payload);
        this.selectedTicketForAction = updated;
        this.showNotification('success', `Ticket #${updated.id} transitioned to ${updated.status} (version ${updated.version})`);
        await this.loadTickets();
        await this.loadDashboard();
      } catch (err) {
        this.ticketActionError = err.message || (err.data && err.data.detail) || "Transition rejected by server.";
      }
    },
    viewTriageExplanation(t) {
      this.activeTriageExplanation = t.triage_explanation || "No explanation recorded.";
    },
    regenerateEventId() {
      this.sensorSim.event_id = 'evt-sim-' + Math.floor(Math.random() * 1000000);
    },
    async sendSensorTelemetry(isRetry) {
      try {
        const payload = {
          source_id: this.sensorSim.source_id,
          event_id: this.sensorSim.event_id,
          metric: this.sensorSim.metric,
          value: this.sensorSim.value,
          observed_at: new Date().toISOString()
        };
        const res = await api.ingestSensorEvent(payload);
        this.sensorResult = res;
        if (res.status === 'duplicate_suppressed') {
          this.showNotification('warning', `Duplicate Event Suppressed: ${res.message}`);
        } else if (res.threshold_breached) {
          this.showNotification('error', `Threshold Breached! Ticket #${res.ticket_id} created (${res.priority}).`);
          await this.loadTickets();
          await this.loadDashboard();
        } else {
          this.showNotification('success', 'Telemetry ingested within nominal parameters.');
        }
      } catch (err) {
        this.sensorResult = { error: err.message, details: err.data };
      }
    },
    openApprovalDialog(item, decision) {
      this.approvalDialogItem = item;
      this.approvalDialogDecision = decision;
      this.approvalReason = decision === 'approved' ? 'Departmental safety protocol and risk assessment validated.' : 'Capacity exceeded.';
      this.approvalError = null;
    },
    async submitApprovalDecision() {
      this.approvalError = null;
      try {
        const payload = {
          request_type: this.approvalDialogItem.type,
          request_id: this.approvalDialogItem.id,
          decision: this.approvalDialogDecision,
          reason: this.approvalReason
        };
        await api.decideApproval(payload);
        this.approvalDialogItem = null;
        this.showNotification('success', `Approval decision (${payload.decision}) successfully executed!`);
        await this.loadPendingApprovals();
        await this.loadDashboard();
        await this.loadFacilities();
        await this.loadLoans();
      } catch (err) {
        this.approvalError = err.message || (err.data && err.data.detail) || "Approval rejected by server.";
      }
    },
    async retryIntegration(id) {
      try {
        const res = await api.retryIntent(id);
        this.showNotification('success', `Intent #${res.id} reconciled! Status: ${res.status}`);
        await this.loadIntents();
      } catch (err) {
        this.showNotification('error', err.message || "Failed to reconcile intent.");
      }
    },
    formatTime(dtStr) {
      if (!dtStr) return '—';
      const d = new Date(dtStr);
      return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
  }
};
</script>
