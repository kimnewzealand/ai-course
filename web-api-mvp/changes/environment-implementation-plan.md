# Implementation Plan: Environment Support Tasks 0 & 1

This plan outlines the step-by-step execution of the two tasks defined in the environment support work item:

- **Task 0**: Add Environment Field to Database Model
- **Task 1**: Implement Environment-Specific E2E Tests

## Task 0: Add Environment Field to Database Model

### Objective
Modify the Item database model to include an environment field that enables multiple versions of the same configuration to exist in different environments.

### Implementation Steps

#### 1.1 Update SQLAlchemy Model (`app/models.py`)
```python
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, UniqueConstraint

class Environment(str, Enum):
    DEVELOPMENT = "development"
    CI = "ci"
    PRODUCTION = "production"

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    environment = Column(SQLEnum(Environment), nullable=False, default=Environment.DEVELOPMENT)
    created_at = Column(String)
    updated_at = Column(String)

    # Ensure (name, environment) uniqueness
    __table_args__ = (
        UniqueConstraint('name', 'environment', name='uq_item_name_environment'),
    )
```

#### 1.2 Update Pydantic Schemas (`app/schemas.py`)
```python
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    CI = "ci"
    PRODUCTION = "production"

class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    environment: Environment = Field(description="Deployment environment")
```

#### 1.3 Recreate Database Tables
Since there's no existing data, simply recreate the database tables with the new schema:

```bash
# Remove existing database files
rm -f web-api-mvp/items.db test_items.db

# Recreate tables with new schema
cd web-api-mvp && python -c "from app.database import init_db; init_db()"
```

#### 1.4 Test Database Changes
```python
# Verify model works with new fields
cd web-api-mvp && python -c "
from app.models import Item, Environment
from app.database import SessionLocal

db = SessionLocal()
# Test creating items with environment
item = Item(name='test', environment=Environment.DEVELOPMENT)
print('Model validation successful')
"
```

### Success Criteria for Task 0
- ✅ Database schema includes environment field with enum constraints
- ✅ Unique constraint prevents duplicate (name, environment) pairs
- ✅ Model and schema definitions updated correctly
- ✅ Database recreation completes successfully

---

## Task 1: Implement Environment-Specific E2E Tests

### Objective
Create E2E tests that validate environment isolation and verify that configurations can exist across multiple environments without conflicts.

### Test Requirements Analysis

**Given**: Core functionality provides environment field support
**When**: E2E tests run environment-specific scenarios
**Then**: Environment isolation validated across UI and API interactions

### Implementation Steps

#### 2.1 Extend Backend Tests (`tests/test_api.py`)
Add new test class for environment functionality:
```python
class TestEnvironmentIsolation:
    def test_same_name_different_environments(self, client):
        """Verify same item name can exist in multiple environments."""
        # Create item in development
        dev_item = client.post("/v1/items", json={
            "name": "test-config",
            "environment": "development"
        }).json()

        # Create item with same name in production
        prod_item = client.post("/v1/items", json={
            "name": "test-config",
            "environment": "production"
        }).json()

        # Verify both exist with different IDs
        assert dev_item["id"] != prod_item["id"]
        assert dev_item["name"] == prod_item["name"]
        assert dev_item["environment"] == "development"
        assert prod_item["environment"] == "production"

    def test_environment_isolation(self, client):
        """Verify operations are isolated by environment."""
        # Create items in different environments
        dev_item = client.post("/v1/items", json={
            "name": "isolated-config",
            "environment": "development"
        })

        # Getting development items should only return dev items
        dev_response = client.get("/v1/items?environment=development")
        dev_items = dev_response.json()
        assert len(dev_items) == 1
        assert dev_items[0]["environment"] == "development"

        # Production items should be empty (no items created there)
        prod_response = client.get("/v1/items?environment=production")
        prod_items = prod_response.json()
        assert len(prod_items) == 0
```

#### 2.2 Update E2E UI Tests (`ui/tests/e2e/item-management.test.ts`)
Add environment-specific test scenarios:
```typescript
test('environment isolation works across UI', async ({ page }) => {
  // Navigate to item management
  await page.goto('/');

  // Select development environment (assuming new dropdown exists)
  await page.selectOption('[data-testid="environment-selector"]', 'development');

  // Create item in development
  await page.fill('[data-testid="item-name"]', 'ui-test-config');
  await page.click('[data-testid="create-item"]');

  // Verify item appears in development list
  await expect(page.locator('[data-testid="item-row"]')).toContainText('development');

  // Switch to production environment
  await page.selectOption('[data-testid="environment-selector"]', 'production');

  // Verify item doesn't appear in production list
  await expect(page.locator('[data-testid="item-row"]')).toHaveCount(0);
});
```

#### 2.3 Run Test Suite
```bash
# Run backend tests
cd web-api-mvp && python -m pytest tests/test_api.py::TestEnvironmentIsolation -v

# Run UI E2E tests (environment selector functionality still TBD)
cd ui && npm run test:e2e
```

### Success Criteria for Task 1
- ✅ E2E tests validate environment isolation works correctly
- ✅ Same configuration names supported across environments
- ✅ Environment-specific operations confirmed (API + UI)
- ✅ Test suite integrates with existing testing infrastructure

---

## Execution Order & Dependencies

### Task Dependencies
- **Task 0** must complete before **Task 1**
- Database schema changes required before testing isolation
- Migration must succeed for tests to run properly

### Estimated Timeline
- **Task 0 (Database Model)**: 1-2 hours
  - Model/schema updates: 30 minutes
  - Database recreation/testing: 30-60 minutes
- **Task 1 (E2E Tests)**: 2-4 hours
  - Backend tests: 1-2 hours
  - E2E UI tests: 1-2 hours

### Risk Assessment
- **Schema Compatibility**: Model changes might break existing code - *Mitigation*: Test model creation directly before full integration
- **Test Dependencies**: Tasks require data layer to be ready - *Mitigation*: Complete Task 0 validation before starting Task 1
- **UI Test Challenges**: Environment selector may not exist in UI yet - *Mitigation*: Focus backend tests first, UI tests can be mock-based initially

## Validation Checklist

### After Task 0
- [ ] Run `uvicorn app.main:app` successfully starts without errors
- [ ] Database table recreation completes without errors
- [ ] Schema validation works for environment enum values
- [ ] Model can create items with environment field

### After Task 1
- [ ] All new environment isolation tests pass
- [ ] Existing test suite still passes (no regressions)
- [ ] Environment-specific operations work as expected
- [ ] Error handling for invalid environments works correctly

---

**Last Updated**: November 30, 2025
**Focus**: Execute the two defined tasks from Work Item 001
