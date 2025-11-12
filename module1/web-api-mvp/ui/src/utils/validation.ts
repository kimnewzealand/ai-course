import { ValidationResult } from '../types/index.js';

export function validateItemName(name: string): string | null {
  if (!name || name.trim().length === 0) {
    return 'Name is required';
  }
  if (name.length > 100) {
    return 'Name must be 100 characters or less';
  }
  return null;
}

export function validateItemDescription(description: string | undefined): string | null {
  if (description && description.length > 500) {
    return 'Description must be 500 characters or less';
  }
  return null;
}

export function validateItemForm(formData: FormData): ValidationResult {
  const name = formData.get('name') as string;
  const description = formData.get('description') as string;

  const errors: Record<string, string> = {};

  const nameError = validateItemName(name);
  if (nameError) errors.name = nameError;

  const descError = validateItemDescription(description);
  if (descError) errors.description = descError;

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
}
