async function globalSetup() {
  // Delete all items from the database before running tests
  const baseUrl = 'http://localhost:8000';
  
  try {
    // Get all items
    const response = await fetch(`${baseUrl}/v1/items?limit=1000`);
    if (response.ok) {
      const items = await response.json();
      
      // Delete each item
      for (const item of items) {
        await fetch(`${baseUrl}/v1/items/${item.id}`, {
          method: 'DELETE',
        });
      }
      
      console.log(`Deleted ${items.length} items from database`);
    }
  } catch (error) {
    console.error('Failed to clean database:', error);
  }
}

export default globalSetup;

