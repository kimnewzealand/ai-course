import { test, expect } from '@playwright/test';

test('should load the admin interface', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('Item Management Admin');
});
