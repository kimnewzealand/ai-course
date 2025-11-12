Here's the comprehensive implementation plan for the admin web interface based on the updated specifications:

## 1. Project Structure (in web-api-mvp/ui/)

```
web-api-mvp/ui/
├── src/
│   ├── components/
│   │   ├── App.ts
│   │   ├── ItemManager.ts
│   │   ├── ItemForm.ts
│   │   ├── ItemList.ts
│   │   └── ApiService.ts
│   ├── types/
│   │   └── index.ts
│   ├── utils/
│   │   └── validation.ts
│   └── styles/
│       ├── main.css
│       └── components.css
├── tests/
│   ├── unit/
│   │   ├── ApiService.test.ts
│   │   ├── validation.test.ts
│   │   └── components.test.ts
│   └── e2e/
│       └── admin-interface.spec.ts
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── playwright.config.ts
├── .env
└── README.md
```

## 2. Dependencies (pnpm packages with specific versions)

```json
{
  "name": "admin-ui",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite --host",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:e2e": "playwright test",
    "lint": "eslint .",
    "format": "prettier --write ."
  },
  "devDependencies": {
    "@types/node": "^20.10.5",
    "@typescript-eslint/eslint-plugin": "^6.15.0",
    "@typescript-eslint/parser": "^6.15.0",
    "eslint": "^8.56.0",
    "jsdom": "^23.2.0",
    "playwright": "^1.40.1",
    "prettier": "^3.1.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.10",
    "vitest": "^1.1.0"
  }
}
```

## 3. Component Architecture

**App.ts**: Main application controller
**ItemManager.ts**: Orchestrates item CRUD operations
**ItemForm.ts**: Form component for creating/editing items
**ItemList.ts**: Display component for listing items
**ApiService.ts**: HTTP client for API communication

## 4. API Integration Using Fetch

Based on `web-api-mvp/app/main.py`, the available endpoints are:

- `GET /items` & `GET /v1/items` - List items
- `POST /items` & `POST /v1/items` - Create item
- `GET /items/{id}` & `GET /v1/items/{id}` - Get item
- `PUT /items/{id}` & `PUT /v1/items/{id}` - Update item
- `DELETE /items/{id}` & `DELETE /v1/items/{id}` - Delete item
- `GET /health` - Health check

**ApiService.ts**:
```typescript
class ApiService {
  private baseUrl = 'http://localhost:8000';

  async getItems(): Promise<Item[]> {
    const response = await fetch(`${this.baseUrl}/items`);
    return response.json();
  }

  async createItem(item: Omit<Item, 'id' | 'created_at' | 'updated_at'>): Promise<Item> {
    const response = await fetch(`${this.baseUrl}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(item)
    });
    return response.json();
  }

  // Similar methods for update, delete
}
```

## 5. Form Handling and Validation

**validation.ts**:
```typescript
export function validateName(name: string): string | null {
  if (!name || name.length < 1) return 'Name is required';
  if (name.length > 100) return 'Name must be 100 characters or less';
  return null;
}

export function validateDescription(desc: string): string | null {
  if (desc && desc.length > 500) return 'Description must be 500 characters or less';
  return null;
}
```

**ItemForm.ts**:
```typescript
export class ItemForm {
  private form: HTMLFormElement;
  private apiService: ApiService;

  constructor(formSelector: string, apiService: ApiService) {
    this.form = document.querySelector(formSelector);
    this.apiService = apiService;
    this.bindEvents();
  }

  private async handleSubmit(event: Event): Promise<void> {
    event.preventDefault();
    const formData = new FormData(this.form);
    const data = {
      name: formData.get('name') as string,
      description: formData.get('description') as string
    };

    // Validate
    const errors = this.validate(data);
    if (Object.keys(errors).length > 0) {
      this.displayErrors(errors);
      return;
    }

    try {
      await this.apiService.createItem(data);
      this.showSuccess('Item created successfully');
      this.form.reset();
    } catch (error) {
      this.showError('Failed to create item');
    }
  }
}
```

## 6. Error Handling and User Feedback

- Network error handling in API calls
- User-friendly error messages
- Loading states during operations
- Success/error toast notifications
- Form validation feedback

## 7. Testing Strategy

**Unit Tests (vitest)**:
- API service methods
- Validation functions
- Form component logic

**Integration Tests (Playwright)**:
- Complete CRUD workflows
- Form submissions
- Error handling scenarios

## 8. Build and Development Setup

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    host: true,
    port: 3000
  },
  test: {
    environment: 'jsdom'
  }
});
```

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  }
}
```

## 9. File Contents and Configuration

**index.html**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Admin Interface</title>
</head>
<body>
  <div id="app">
    <h1>Item Management</h1>
    <div id="item-form"></div>
    <div id="item-list"></div>
  </div>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

**README.md**:
```markdown
# Admin UI

## Setup
1. Install pnpm
2. Run `pnpm install`
3. Copy `.env.example` to `.env`
4. Run `pnpm dev`

## API
Connects to REST API at http://localhost:8000
```

This plan provides a complete blueprint for building the admin interface using vanilla TypeScript, with proper separation of concerns, comprehensive testing, and modern development practices.