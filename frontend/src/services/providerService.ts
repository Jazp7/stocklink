// providerService.ts — Adding trailing slash to avoid redirects
import type { ApiResponse } from '../types/apiTypes';
import type { Provider, ProviderCreate, ProviderUpdate } from '../types/providerTypes';

const API_URL = import.meta.env.VITE_API_URL;

export const providerService = {
  async getAll(page: number = 1, limit: number = 10): Promise<ApiResponse<Provider[]>> {
    // We add the / here: /providers/
    const response = await fetch(`${API_URL}/providers/?page=${page}&limit=${limit}`);
    return response.json();
  },

  async getById(id: number): Promise<ApiResponse<Provider>> {
    const response = await fetch(`${API_URL}/providers/${id}`);
    return response.json();
  },

  async create(provider: ProviderCreate): Promise<ApiResponse<Provider>> {
    const response = await fetch(`${API_URL}/providers/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(provider),
    });
    return response.json();
  },

  async update(id: number, provider: ProviderUpdate): Promise<ApiResponse<Provider>> {
    const response = await fetch(`${API_URL}/providers/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(provider),
    });
    return response.json();
  },

  async delete(id: number): Promise<ApiResponse<void>> {
    const response = await fetch(`${API_URL}/providers/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  }
};
