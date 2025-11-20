// Configuration value types
export type ConfigValue = string | number | boolean | Record<string, unknown>;

export interface ConfigItem {
  id: number;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt?: string;
}

// Create/Update request types
export interface CreateConfig {
  name: string;
  description?: string;
}

export interface UpdateConfig {
  name?: string;
  description?: string;
}

// Client configuration
export interface ConfigClientOptions {
  baseUrl: string;
  timeout?: number;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiListResponse<T> {
  data: T[];
  total?: number;
  page?: number;
  limit?: number;
}

// Error types
export class ConfigClientError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public code?: string
  ) {
    super(message);
    this.name = 'ConfigClientError';
  }
}
