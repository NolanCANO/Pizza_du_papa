export interface StockItem {
  id: number;
  ingredient: string;
  quantity: number;
}

export interface StockItemCreate {
  ingredient: string;
  quantity: number;
}

export interface StockUpdate {
  quantity_change: number;
}
