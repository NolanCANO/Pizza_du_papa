export interface Pizza {
  id: number;
  name: string;
  description: string;
  price: number;
  is_available: boolean;
}

export interface PizzaCreate {
  name: string;
  description: string;
  price: number;
  is_available?: boolean;
}
