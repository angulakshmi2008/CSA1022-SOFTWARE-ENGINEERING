/**
 * Centralized API Client for Smart Campus Platform.
 * Supports token authentication, role switching for demonstrations,
 * and standard RFC error formatting.
 */

const API_BASE = '/api';

// Current active demo user token and profile stored in memory
let currentToken = null;
let currentUser = null;

export const setAuthSession = (token, user) => {
  currentToken = token;
  currentUser = user;
  localStorage.setItem('campus_token', token);
  localStorage.setItem('campus_user', JSON.stringify(user));
};

export const getAuthToken = () => {
  if (!currentToken) {
    currentToken = localStorage.getItem('campus_token');
  }
  return currentToken;
};

export const getCurrentUser = () => {
  if (!currentUser) {
    const raw = localStorage.getItem('campus_user');
    if (raw) {
      try {
        currentUser = JSON.parse(raw);
      } catch (e) {
        currentUser = null;
      }
    }
  }
  return currentUser;
};

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const token = getAuthToken();

  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...(options.headers || {})
  };

  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }

  const config = {
    ...options,
    headers
  };

  if (options.body && typeof options.body === 'object') {
    config.body = JSON.stringify(options.body);
  }

  try {
    const res = await fetch(url, config);
    let data = null;
    const contentType = res.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      data = await res.json();
    } else {
      data = await res.text();
    }

    if (!res.ok) {
      const errorObj = {
        status: res.status,
        statusText: res.statusText,
        data: data || {},
        message: (data && (data.error || data.detail || (data.resolution_notes && data.resolution_notes[0]))) || `HTTP ${res.status}: ${res.statusText}`
      };
      throw errorObj;
    }
    return data;
  } catch (err) {
    console.error(`API Error on [${options.method || 'GET'} ${endpoint}]:`, err);
    throw err;
  }
}

export const api = {
  // Auth
  login: (username, password) => request('/auth/login/', { method: 'POST', body: { username, password } }),
  logout: () => request('/auth/logout/', { method: 'POST' }),
  getMe: () => request('/auth/me/'),
  getUsers: (params = '') => request(`/auth/users/${params ? '?' + params : ''}`),

  // Campuses & Facilities
  getCampuses: () => request('/campuses/'),
  getFacilities: (params = '') => request(`/facilities/${params ? '?' + params : ''}`),

  // Bookings
  getBookings: (params = '') => request(`/bookings/${params ? '?' + params : ''}`),
  getCalendar: (params = '') => request(`/bookings/calendar/${params ? '?' + params : ''}`),
  getMyBookings: () => request('/bookings/my-bookings/'),
  createBooking: (data) => request('/bookings/', { method: 'POST', body: data }),
  updateBookingStatus: (id, data) => request(`/bookings/${id}/status/`, { method: 'PATCH', body: data }),

  // Maintenance & Triage
  getTickets: (params = '') => request(`/tickets/${params ? '?' + params : ''}`),
  getTicket: (id) => request(`/tickets/${id}/`),
  createTicket: (data) => request('/tickets/', { method: 'POST', body: data }),
  updateTicketState: (id, data) => request(`/tickets/${id}/state/`, { method: 'PATCH', body: data }),
  assignTechnician: (id, assignee_id) => request(`/tickets/${id}/assign/`, { method: 'PATCH', body: { assignee_id } }),
  addInspection: (id, data) => request(`/tickets/${id}/inspections/`, { method: 'POST', body: data }),
  getSLAPolicies: () => request('/tickets/sla-policies/'),

  // Sensor Telemetry
  ingestSensorEvent: (data) => request('/sensor-events/', { method: 'POST', body: data }),
  getSensorHistory: () => request('/sensor-events/history/'),

  // Approvals
  getPendingApprovals: () => request('/approvals/pending/'),
  getApprovalHistory: () => request('/approvals/'),
  decideApproval: (data) => request('/approvals/', { method: 'POST', body: data }),

  // Equipment Loans
  getEquipmentLoans: () => request('/equipment-loans/'),
  createEquipmentLoan: (data) => request('/equipment-loans/', { method: 'POST', body: data }),

  // DevOps & Integrations
  getIntents: () => request('/integration-intents/'),
  createIntent: (data) => request('/integration-intents/', { method: 'POST', body: data }),
  retryIntent: (id) => request(`/integration-intents/${id}/retry/`, { method: 'POST' }),

  // Audit & Dashboard
  getDashboardSummary: (campus_id = '') => request(`/dashboard/summary/${campus_id ? '?campus=' + campus_id : ''}`),
  getAuditEvents: (params = '') => request(`/audit-events/${params ? '?' + params : ''}`),
  getHealth: () => request('/health/')
};
