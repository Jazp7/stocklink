// dashboardService.ts — Functions to fetch statistics for the dashboard
import type { ApiResponse } from '../types/apiTypes';

const API_URL = 'http://127.0.0.1:8000';

export type DashboardStats = {
  total_products: number;
  total_providers: number;
  total_value: number;
  out_of_stock: number;
  low_stock: number;
};

export const dashboardService = {
  async getStats(): Promise<ApiResponse<DashboardStats>> {
    // Adding trailing slash to avoid redirects
    const response = await fetch(`${API_URL}/dashboard/stats/`);
    return response.json();
  }
};
