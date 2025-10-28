export interface Delivery {
  id: number;
  order_id: number;
  assigned_driver: string;
  status: DeliveryStatus;
  eta_minutes: number;
  created_at: string;
}

export interface DeliveryCreate {
  order_id: number;
  assigned_driver: string;
  eta_minutes: number;
}

export type DeliveryStatus = 'PENDING' | 'PICKED_UP' | 'DELIVERED';
