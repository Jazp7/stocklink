// provider.ts — TypeScript types for Providers
export type Provider = {
  id: number;
  name: string;
  email: string;
  address?: string;
  phone?: string;
  description?: string;
  created_at: string;
  updated_at: string;
};

export type ProviderCreate = {
  name: string;
  email: string;
  address?: string;
  phone?: string;
  description?: string;
};

export type ProviderUpdate = {
  name?: string;
  email?: string;
  address?: string;
  phone?: string;
  description?: string;
};
