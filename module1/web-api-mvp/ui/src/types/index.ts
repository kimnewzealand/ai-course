export interface Item {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface ItemCreate {
  name: string;
  description?: string;
}

export interface ItemUpdate {
  name: string;
  description?: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}
