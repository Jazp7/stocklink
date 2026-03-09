// providerService.ts — Updated imports
import type { ApiResponse } from '../types/apiTypes';
import type { Provider, ProviderCreate, ProviderUpdate } from '../types/providerTypes';

const API_URL = 'http://127.0.0.1:8000';

export const providerService = {
  async getAll(): Promise<ApiResponse<Provider[]>> {
    const response = await fetch(`${API_URL}/providers`);
    return response.json();
  },
  async create(provider: ProviderCreate): Promise<ApiResponse<Provider>> {
    const response = await fetch(`${API_URL}/providers`, {
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
