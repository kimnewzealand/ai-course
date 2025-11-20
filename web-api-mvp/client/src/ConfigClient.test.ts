import { ConfigClient } from './ConfigClient';
import { ConfigClientError } from './types';

describe('ConfigClient', () => {
  let client: ConfigClient;

  beforeEach(() => {
    client = new ConfigClient({
      baseUrl: 'http://localhost:8000',
      timeout: 1000
    });
  });

  describe('initialization', () => {
    it('should create a client instance', () => {
      expect(client).toBeInstanceOf(ConfigClient);
    });

    it('should accept custom timeout', () => {
      const customClient = new ConfigClient({
        baseUrl: 'http://localhost:8000',
        timeout: 5000
      });
      expect(customClient).toBeDefined();
    });
  });

  describe('error handling', () => {
    it('should create proper error messages', () => {
      const error = new ConfigClientError('Test error', 404, 'NOT_FOUND');
      expect(error.message).toBe('Test error');
      expect(error.statusCode).toBe(404);
      expect(error.code).toBe('NOT_FOUND');
      expect(error.name).toBe('ConfigClientError');
    });
  });

  // Note: Integration tests with real API would go here
  // They would be skipped if the API server isn't running
});
