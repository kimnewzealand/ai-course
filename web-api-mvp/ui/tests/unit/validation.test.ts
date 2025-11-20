import { describe, it, expect } from 'vitest';
import { validateItemName, validateItemDescription, validateItemForm } from '../../src/utils/validation.js';

describe('Validation', () => {
  describe('validateItemName', () => {
    it('should return null for valid names', () => {
      expect(validateItemName('Valid Name')).toBeNull();
      expect(validateItemName('A')).toBeNull();
      expect(validateItemName('a'.repeat(100))).toBeNull();
    });

    it('should return error for empty names', () => {
      expect(validateItemName('')).toBe('Name is required');
      expect(validateItemName('   ')).toBe('Name is required');
    });

    it('should return error for names too long', () => {
      expect(validateItemName('a'.repeat(101))).toBe('Name must be 100 characters or less');
    });

    it('should return error for null/undefined', () => {
      expect(validateItemName(null as any)).toBe('Name is required');
      expect(validateItemName(undefined as any)).toBe('Name is required');
    });
  });

  describe('validateItemDescription', () => {
    it('should return null for valid descriptions', () => {
      expect(validateItemDescription('')).toBeNull();
      expect(validateItemDescription('Valid description')).toBeNull();
      expect(validateItemDescription('a'.repeat(500))).toBeNull();
    });

    it('should return error for descriptions too long', () => {
      expect(validateItemDescription('a'.repeat(501))).toBe('Description must be 500 characters or less');
    });

    it('should return null for undefined description', () => {
      expect(validateItemDescription(undefined)).toBeNull();
    });
  });

  describe('validateItemForm', () => {
    it('should return valid result for correct data', () => {
      const formData = new FormData();
      formData.append('name', 'Test Item');
      formData.append('description', 'Test Description');

      const result = validateItemForm(formData);
      expect(result.isValid).toBe(true);
      expect(result.errors).toEqual({});
    });

    it('should return invalid result with errors', () => {
      const formData = new FormData();
      formData.append('name', ''); // Invalid
      formData.append('description', 'a'.repeat(501)); // Invalid

      const result = validateItemForm(formData);
      expect(result.isValid).toBe(false);
      expect(result.errors.name).toBe('Name is required');
      expect(result.errors.description).toBe('Description must be 500 characters or less');
    });
  });
});
