const API_BASE = '/api';

let currentToken: string = '';

export function setAuthToken(token: string) {
  currentToken = token;
}

export function getAuthToken(): string {
  return currentToken;
}

async function request(endpoint: string, options: RequestInit = {}) {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };
  
  if (currentToken && !headers['Authorization']) {
    headers['Authorization'] = `Bearer ${currentToken}`;
  }
  
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });
  
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || `Request failed with status ${res.status}`);
  }
  return data;
}

export const api = {
  // Auth
  login: (username: string, password: string) => 
    request('/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) }),
  getProfile: () => request('/auth/me'),

  // Products
  getProducts: (regionId: string = 'US-EAST') => 
    request(`/products/?region_id=${regionId}`),

  // Orders
  getOrders: (regionId?: string) => 
    request(regionId ? `/orders/?region_id=${regionId}` : '/orders/'),
  getOrder: (id: string) => request(`/orders/${id}`),
  placeOrder: (items: { sku: string; quantity: number }[], regionId: string) =>
    request('/orders/', { method: 'POST', body: JSON.stringify({ items, region_id: regionId }) }),
  cancelOrder: (id: string) =>
    request(`/orders/${id}/cancel`, { method: 'POST' }),

  // Payments (Mock Webhook Trigger)
  submitPaymentCallback: (payload: any, signature: string) =>
    request('/payments/callback', {
      method: 'POST',
      headers: { 'X-Signature': signature },
      body: JSON.stringify(payload)
    }),

  // Refunds
  getRefunds: () => request('/refunds/'),
  requestRefund: (orderId: string, amount: number, reason: string) =>
    request('/refunds/', { method: 'POST', body: JSON.stringify({ order_id: orderId, amount, reason }) }),
  decideRefund: (refundId: string, decision: 'APPROVE' | 'REJECT', notes?: string) =>
    request(`/refunds/${refundId}/decide`, { method: 'POST', body: JSON.stringify({ decision, notes }) }),
  executeRefund: (refundId: string, simulateFailure: boolean = false) =>
    request(`/refunds/${refundId}/execute`, { method: 'POST', body: JSON.stringify({ simulate_gateway_failure: simulateFailure }) }),

  // Warehouse
  getPickLists: () => request('/warehouse/pick-lists'),
  packOrder: (orderId: string) => request(`/warehouse/orders/${orderId}/pack`, { method: 'POST' }),
  dispatchOrder: (orderId: string) => request(`/warehouse/orders/${orderId}/dispatch`, { method: 'POST' }),

  // Scanner
  syncScannerBatch: (events: any[]) =>
    request('/scanner/sync-batch', { method: 'POST', body: JSON.stringify({ events }) }),

  // Policies
  getPolicies: () => request('/policies/'),
  updatePolicy: (regionId: string, data: { tax_rate: number; shipping_fee: number; refund_approval_threshold: number }) =>
    request(`/policies/${regionId}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Reporting
  getReportSummary: () => request('/reporting/summary'),
  getHealth: () => fetch('/health').then(r => r.json())
};
