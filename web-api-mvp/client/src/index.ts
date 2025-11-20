// Main exports from the configuration client library
export { ConfigClient } from './ConfigClient';
export * from './types';

// Re-export for convenience
export type {
  ConfigItem,
  CreateConfig,
  UpdateConfig,
  ConfigClientOptions,
  ConfigClientError
} from './types';
