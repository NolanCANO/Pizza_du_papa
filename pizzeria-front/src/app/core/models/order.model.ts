export interface OrderItem {
  pizza_id: number;
  quantity: number;
}

export interface OrderItemResponse {
  pizza_id: number;
  quantity: number;
  unit_price: number;
  line_total: number;
}

export interface Order {
  id: number;
  customer_name: string;
  delivery_address: string;
  status: OrderStatus;
  total_price: number;
  items: OrderItemResponse[];
  created_at: string;
}

export interface OrderCreate {
  customer_name: string;
  delivery_address: string;
  items: OrderItem[];
}

export type OrderStatus = 'PENDING' | 'PREPARING' | 'OUT_FOR_DELIVERY' | 'DELIVERED' | 'CANCELLED';
