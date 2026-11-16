export type UserRole = 
  | 'CUSTOMER' 
  | 'PICKER' 
  | 'SUPPORT_AGENT' 
  | 'FINANCE_REVIEWER' 
  | 'STORE_MANAGER' 
  | 'ADMINISTRATOR';

export interface Product {
  sku: string;
  name: string;
  description: string;
  base_price: number;
  category: string;
  on_hand: number;
  reserved: number;
  available_stock: number;
}

export interface OrderLine {
  line_id: string;
  sku: string;
  quantity: number;
  unit_price: number;
  tax_rate: number;
  tax_amount: number;
  line_total: number;
}

export interface Order {
  order_id: string;
  owner_id: string;
  state: 'PLACED' | 'PAID' | 'PACKED' | 'DISPATCHED' | 'DELIVERED' | 'CLOSED' | 'CANCELLED' | 'NEEDS_REFUND';
  region_id: string;
  policy_version: number;
  subtotal: number;
  tax_amount: number;
  shipping_fee: number;
  total_amount: number;
  dispatch_due_at?: string;
  created_at: string;
  updated_at: string;
  items?: OrderLine[];
}

export interface RefundRequest {
  refund_id: string;
  order_id: string;
  amount: number;
  state: 'REQUESTED' | 'APPROVED' | 'REJECTED' | 'EXECUTING' | 'FAILED' | 'EXECUTED';
  reason: string;
  requested_by: string;
  approved_by?: string;
  idempotency_key: string;
  failure_reason?: string;
  created_at: string;
  resolved_at?: string;
}

export interface RegionalPolicy {
  region_id: string;
  region_name: string;
  policy_version: number;
  tax_rate: number;
  shipping_fee: number;
  refund_approval_threshold: number;
  is_active: boolean;
}

export interface ScannerEvent {
  node_id: string;
  event_id: string;
  sku: string;
  region_id: string;
  event_type: 'STOCK_COUNT' | 'RECEIVE' | 'PICK_VERIFY';
  quantity: number;
  observation_time: string;
  schema_version: string;
}
