// product.ts — TypeScript types for Products
export type Product = {
  id: number;
  name: string;
  price: number;
  stock_quantity: number;
  category: string;
  description?: string;
  provider_id: number;
  created_at: string;
  updated_at: string;
};

export type ProductCreate = {
  name: string;
  price: number;
  stock_quantity: number;
  category: string;
  description?: string;
  provider_id: number;
};

export type ProductUpdate = {
  name?: string;
  price?: number;
  stock_quantity?: number;
  category?: string;
  description?: string;
  provider_id?: number;
};
