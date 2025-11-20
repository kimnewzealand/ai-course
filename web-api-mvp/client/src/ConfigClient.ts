import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  ConfigItem,
  CreateConfig,
  UpdateConfig,
  ConfigClientOptions,
  ConfigClientError
} from './types';

export class ConfigClient {
  private axiosInstance: AxiosInstance;

  constructor(options: ConfigClientOptions) {
    this.axiosInstance = axios.create({
      baseURL: `${options.baseUrl}/v1`,
      timeout: options.timeout || 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Error handling interceptor
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          // Server responded with error status
          const statusCode = error.response.status;
          let message = 'Unknown error occurred';

          if (statusCode === 404) {
            message = 'Configuration not found';
          } else if (statusCode === 422) {
            message = 'Invalid configuration data provided';
          } else if (statusCode >= 500) {
            message = 'Server error occurred';
          }

          throw new ConfigClientError(message, statusCode, error.code);
        } else if (error.request) {
          // Network error
          throw new ConfigClientError('Network error - unable to reach server', undefined, 'NETWORK_ERROR');
        } else {
          // Setup error
          throw new ConfigClientError(error.message || 'Client setup error');
        }
      }
    );
  }

  // Get all configurations
  async getConfigs(limit?: number, offset?: number): Promise<ConfigItem[]> {
    try {
      let url = '/items';
      const params: any = {};

      if (limit) params.limit = limit;
      if (offset) params.offset = offset;

      const response: AxiosResponse = await this.axiosInstance.get(url, { params });
      return response.data;
    } catch (error) {
      throw error instanceof ConfigClientError ? error : new ConfigClientError('Failed to fetch configurations');
    }
  }

  // Get a specific configuration by ID
  async getConfig(id: number): Promise<ConfigItem> {
    try {
      const response: AxiosResponse = await this.axiosInstance.get(`/items/${id}`);
      return response.data;
    } catch (error) {
      throw error instanceof ConfigClientError ? error : new ConfigClientError('Failed to fetch configuration');
    }
  }

  // Create a new configuration
  async createConfig(config: CreateConfig): Promise<ConfigItem> {
    try {
      const response: AxiosResponse = await this.axiosInstance.post('/items', config);
      return response.data;
    } catch (error) {
      throw error instanceof ConfigClientError ? error : new ConfigClientError('Failed to create configuration');
    }
  }

  // Update an existing configuration
  async updateConfig(id: number, config: UpdateConfig): Promise<ConfigItem> {
    try {
      const response: AxiosResponse = await this.axiosInstance.put(`/items/${id}`, config);
      return response.data;
    } catch (error) {
      throw error instanceof ConfigClientError ? error : new ConfigClientError('Failed to update configuration');
    }
  }

  // Delete a configuration
  async deleteConfig(id: number): Promise<void> {
    try {
      await this.axiosInstance.delete(`/items/${id}`);
    } catch (error) {
      throw error instanceof ConfigClientError ? error : new ConfigClientError('Failed to delete configuration');
    }
  }

  // Create a new client with different options (useful for baseUrl changes)
  createClient(options: Partial<ConfigClientOptions>): ConfigClient {
    return new ConfigClient({
      ...{ baseUrl: this.axiosInstance.defaults.baseURL!.replace('/v1', '') },
      ...options
    });
  }
}
