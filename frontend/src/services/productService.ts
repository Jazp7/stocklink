// productService.ts — Updated imports
import type { ApiResponse } from '../types/apiTypes';
import type { Product, ProductCreate, ProductUpdate } from '../types/productTypes';

const API_URL = 'http://127.0.0.1:8000';

export const productService = {
  async getAll(): Promise<ApiResponse<Product[]>> {
    const response = await fetch(`${API_URL}/products`);
    return response.json();
  },
  async create(product: ProductCreate): Promise<ApiResponse<Product>> {
    const response = await fetch(`${API_URL}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product),
    });
    return response.json();
  },
  async update(id: number, product: ProductUpdate): Promise<ApiResponse<Product>> {
    const response = await fetch(`${API_URL}/products/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product),
    });
    return response.json();
  },
  async delete(id: number): Promise<ApiResponse<void>> {
    const response = await fetch(`${API_URL}/products/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  }
};
