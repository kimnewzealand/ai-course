import { test, expect } from '@playwright/test';

test.describe('Item Management', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test.afterEach(async () => {
    // Clean up all items after each test
    const baseUrl = 'http://localhost:8000';
    try {
      const response = await fetch(`${baseUrl}/v1/items?limit=1000`);
      if (response.ok) {
        const items = await response.json();
        for (const item of items) {
          await fetch(`${baseUrl}/v1/items/${item.id}`, {
            method: 'DELETE',
          });
        }
      }
    } catch (error) {
      console.error('Failed to clean up items:', error);
    }
  });

  test('should load the admin interface', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Item Management Admin');
    await expect(page.locator('#list-btn')).toBeVisible();
    await expect(page.locator('#create-btn')).toBeVisible();
  });

  test('should display empty items list initially', async ({ page }) => {
    await expect(page.locator('#items-container')).toContainText('No items found');
  });

  test('should create a new item', async ({ page }) => {
    // Click create button
    await page.click('#create-btn');

    // Fill form
    await page.fill('#name', 'Test Item');
    await page.fill('#description', 'Test Description');

    // Submit
    await page.click('#submit-btn');

    // Check if item appears in list
    await expect(page.locator('#items-container')).toContainText('Test Item');
    await expect(page.locator('#items-container')).toContainText('Test Description');
  });

  test('should edit an existing item', async ({ page }) => {
    // First create an item
    await page.click('#create-btn');
    await page.fill('#name', 'Original Item');
    await page.fill('#description', 'Original Description');
    await page.click('#submit-btn');

    // Click edit button (first row)
    await page.click('.edit-btn');

    // Modify form
    await page.fill('#name', 'Updated Item');
    await page.fill('#description', 'Updated Description');
    await page.click('#submit-btn');

    // Verify update
    await expect(page.locator('#items-container')).toContainText('Updated Item');
    await expect(page.locator('#items-container')).toContainText('Updated Description');
  });

  test('should delete an item', async ({ page }) => {
    // First create an item
    await page.click('#create-btn');
    await page.fill('#name', 'Item to Delete');
    await page.click('#submit-btn');

    // Click delete button
    page.on('dialog', dialog => dialog.accept()); // Accept confirmation
    await page.click('.delete-btn');

    // Verify item is gone
    await expect(page.locator('#items-container')).toContainText('No items found');
  });

  test('should validate form inputs', async ({ page }) => {
    // Click create button
    await page.click('#create-btn');

    // Try to submit empty form
    await page.click('#submit-btn');

    // Check for validation error
    await expect(page.locator('#name-error')).toContainText('Name is required');

    // Fill invalid data
    await page.fill('#name', 'a'.repeat(101)); // Too long
    await page.fill('#description', 'b'.repeat(501)); // Too long
    await page.click('#submit-btn');

    // Check validation errors
    await expect(page.locator('#name-error')).toContainText('100 characters or less');
    await expect(page.locator('#description-error')).toContainText('500 characters or less');
  });

  test('should cancel form editing', async ({ page }) => {
    // Click create button
    await page.click('#create-btn');

    // Fill some data
    await page.fill('#name', 'Cancelled Item');

    // Click cancel
    await page.click('#cancel-btn');

    // Should return to list view
    await expect(page.locator('#item-list')).not.toHaveClass(/hidden/);
    await expect(page.locator('#item-form')).toHaveClass(/hidden/);
  });
});
