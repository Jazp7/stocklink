// apiTypes.ts — Using 'type' instead of 'interface' for better compatibility
export type ApiResponse<T> = {
  success: boolean;
  data: T;
  pagination?: {
    page: number;
    limit: number;
    total_items: number;
    total_pages: number;
  };
  error?: {
    code: string;
    message: string;
    details: any[];
  };
};
