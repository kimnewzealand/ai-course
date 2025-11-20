import { ApiService } from './components/ApiService.js';
import { validateItemForm } from './utils/validation.js';
import { Item } from './types/index.js';

class App {
  private apiService: ApiService;
  private currentView: 'list' | 'form' = 'list';

  constructor() {
    this.apiService = new ApiService();
    this.bindEvents();
  }

  async init(): Promise<void> {
    await this.showItemList();
  }

  private bindEvents(): void {
    const listBtn = document.getElementById('list-btn') as HTMLButtonElement;
    const createBtn = document.getElementById('create-btn') as HTMLButtonElement;
    const cancelBtn = document.getElementById('cancel-btn') as HTMLButtonElement;
    const form = document.getElementById('item-form-element') as HTMLFormElement;

    listBtn.addEventListener('click', () => this.showItemList());
    createBtn.addEventListener('click', () => this.showItemForm());
    cancelBtn.addEventListener('click', () => this.showItemList());
    form.addEventListener('submit', (e) => this.handleFormSubmit(e));
  }

  private async showItemList(): Promise<void> {
    this.currentView = 'list';
    this.updateViewVisibility();

    try {
      const items = await this.apiService.getItems();
      this.renderItemList(items);
    } catch (error) {
      this.renderItemList([]); // Render empty state on error
      this.showNotification('Failed to load items', 'error');
    }
  }

  private showItemForm(item?: Item): void {
    this.currentView = 'form';
    this.updateViewVisibility();

    const form = document.getElementById('item-form-element') as HTMLFormElement;
    const submitBtn = document.getElementById('submit-btn') as HTMLButtonElement;

    if (item) {
      (document.getElementById('name') as HTMLInputElement).value = item.name;
      (document.getElementById('description') as HTMLTextAreaElement).value = item.description || '';
      submitBtn.textContent = 'Update Item';
      form.dataset.itemId = item.id.toString();
    } else {
      form.reset();
      submitBtn.textContent = 'Create Item';
      delete form.dataset.itemId;
    }
  }

  private updateViewVisibility(): void {
    const listSection = document.getElementById('item-list') as HTMLElement;
    const formSection = document.getElementById('item-form') as HTMLElement;

    if (this.currentView === 'list') {
      listSection.classList.remove('hidden');
      formSection.classList.add('hidden');
    } else {
      listSection.classList.add('hidden');
      formSection.classList.remove('hidden');
    }
  }

  private async handleFormSubmit(event: Event): Promise<void> {
    event.preventDefault();

    const form = event.target as HTMLFormElement;
    const formData = new FormData(form);

    // Validate
    const validation = validateItemForm(formData);
    this.displayErrors(validation.errors);

    if (!validation.isValid) {
      return;
    }

    const itemData = {
      name: formData.get('name') as string,
      description: formData.get('description') as string || undefined,
    };

    try {
      const itemId = form.dataset.itemId;
      if (itemId) {
        await this.apiService.updateItem(parseInt(itemId), itemData);
        this.showNotification('Item updated successfully', 'success');
      } else {
        await this.apiService.createItem(itemData);
        this.showNotification('Item created successfully', 'success');
      }
      await this.showItemList();
    } catch (error) {
      this.showNotification('Failed to save item', 'error');
    }
  }

  private renderItemList(items: Item[]): void {
    const container = document.getElementById('items-container') as HTMLElement;
    container.innerHTML = '';

    if (items.length === 0) {
      container.innerHTML = '<p>No items found</p>';
      return;
    }

    const table = document.createElement('table');
    table.innerHTML = `
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Description</th>
          <th>Created</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody')!;
    items.forEach(item => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${item.id}</td>
        <td>${item.name}</td>
        <td>${item.description || ''}</td>
        <td>${new Date(item.created_at).toLocaleDateString()}</td>
        <td>
          <button class="edit-btn" data-id="${item.id}">Edit</button>
          <button class="delete-btn" data-id="${item.id}">Delete</button>
        </td>
      `;

      // Bind events
      const editBtn = row.querySelector('.edit-btn') as HTMLButtonElement;
      const deleteBtn = row.querySelector('.delete-btn') as HTMLButtonElement;

      editBtn.addEventListener('click', () => this.editItem(item));
      deleteBtn.addEventListener('click', () => this.deleteItem(item.id));

      tbody.appendChild(row);
    });

    container.appendChild(table);
  }

  private editItem(item: Item): void {
    this.showItemForm(item);
  }

  private async deleteItem(id: number): Promise<void> {
    if (!confirm('Are you sure you want to delete this item?')) {
      return;
    }

    try {
      await this.apiService.deleteItem(id);
      this.showNotification('Item deleted successfully', 'success');
      await this.showItemList();
    } catch (error) {
      this.showNotification('Failed to delete item', 'error');
    }
  }

  private displayErrors(errors: Record<string, string>): void {
    // Clear previous errors
    document.querySelectorAll('.error').forEach(el => {
      el.textContent = '';
    });

    // Display new errors
    Object.entries(errors).forEach(([field, message]) => {
      const errorEl = document.getElementById(`${field}-error`);
      if (errorEl) {
        errorEl.textContent = message;
      }
    });
  }

  private showNotification(message: string, type: 'success' | 'error' = 'success'): void {
    const notifications = document.getElementById('notifications') as HTMLElement;
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    notifications.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
      notification.remove();
    }, 5000);
  }
}

// Initialize app
const app = new App();
app.init().catch(console.error);
