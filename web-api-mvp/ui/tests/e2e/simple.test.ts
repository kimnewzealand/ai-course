import { test, expect } from '@playwright/test';

test('loads page', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Item Management/);
});

