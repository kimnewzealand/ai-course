import { Item, ItemCreate, ItemUpdate } from '../types/index.js';

export class ApiService {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || 'http://localhost:8000';
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async getItems(): Promise<Item[]> {
    return this.request('/v1/items');
  }

  async getItem(id: number): Promise<Item> {
    return this.request(`/v1/items/${id}`);
  }

  async createItem(item: ItemCreate): Promise<Item> {
    return this.request('/v1/items', {
      method: 'POST',
      body: JSON.stringify(item),
    });
  }

  async updateItem(id: number, item: ItemUpdate): Promise<Item> {
    return this.request(`/v1/items/${id}`, {
      method: 'PUT',
      body: JSON.stringify(item),
    });
  }

  async deleteItem(id: number): Promise<void> {
    return this.request(`/v1/items/${id}`, {
      method: 'DELETE',
    });
  }
}
