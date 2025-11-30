import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app

# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test_items.db"


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine for the entire test session."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=None,  # Disable connection pooling for easier cleanup
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def setup_database(test_engine):
    """Create all tables before tests and drop them after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()  # Ensure engine is disposed before file deletion

    # Clean up test database file with retry logic
    import time

    for attempt in range(3):
        try:
            if os.path.exists("test_items.db"):
                os.remove("test_items.db")
            break
        except PermissionError:
            if attempt < 2:
                time.sleep(0.1)  # Wait briefly and retry
            # If still fails after retries, ignore (file will be overwritten next run)


@pytest.fixture
def db_session(test_engine, setup_database):
    """Create a new database session for each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create a test client with database session override."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    from app.main import get_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_item_data():
    """Fixture providing sample item data for tests."""
    return {"name": "Test Item", "description": "Test Description"}


@pytest.fixture
def sample_item_data_alt():
    """Fixture providing alternative sample item data for tests."""
    return {"name": "Another Item", "description": "Another Description"}


@pytest.fixture
def created_item(client, sample_item_data):
    """Fixture that creates an item and returns its data."""
    response = client.post("/v1/items", json=sample_item_data)
    return response.json()


class TestItemCreation:
    """Test cases for creating items."""

    def test_create_item_success(self, client, sample_item_data):
        """Test successful item creation with valid data."""
        response = client.post("/v1/items", json=sample_item_data)

        assert response.status_code == 200
        data = response.json()

        # Validate all response fields
        assert data["name"] == sample_item_data["name"]
        assert data["description"] == sample_item_data["description"]
        assert "id" in data
        assert isinstance(data["id"], int)
        assert "created_at" in data
        assert isinstance(data["created_at"], str)
        assert data["updated_at"] is None

    def test_create_item_minimal(self, client):
        """Test creating item with minimal required fields."""
        response = client.post("/v1/items", json={"name": "Minimal Item"})

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Minimal Item"
        assert data["description"] is None


class TestItemRetrieval:
    """Test cases for retrieving items."""

    def test_get_items_empty(self, client):
        """Test getting items when database is empty."""
        response = client.get("/v1/items")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

    def test_get_items_with_data(self, client, sample_item_data, sample_item_data_alt):
        """Test getting items when database has data."""
        # Create multiple items
        client.post("/v1/items", json=sample_item_data)
        client.post("/v1/items", json=sample_item_data_alt)

        response = client.get("/v1/items")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_get_items_pagination(self, client, sample_item_data):
        """Test pagination parameters for getting items."""
        # Create 5 items
        for i in range(5):
            client.post(
                "/v1/items", json={"name": f"Item {i}", "description": f"Desc {i}"}
            )

        # Test limit
        response = client.get("/v1/items?limit=3")
        assert response.status_code == 200
        assert len(response.json()) == 3

        # Test offset
        response = client.get("/v1/items?offset=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_item_by_id_success(self, client, created_item):
        """Test retrieving a specific item by ID."""
        item_id = created_item["id"]
        response = client.get(f"/v1/items/{item_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == created_item["name"]
        assert data["description"] == created_item["description"]
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_item_not_found(self, client):
        """Test retrieving non-existent item returns 404."""
        response = client.get("/v1/items/999")

        assert response.status_code == 404
        assert "detail" in response.json()


class TestItemUpdate:
    """Test cases for updating items."""

    def test_update_item_success(self, client, created_item):
        """Test successful item update."""
        item_id = created_item["id"]
        update_data = {"name": "Updated Item", "description": "Updated Description"}

        response = client.put(f"/v1/items/{item_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["updated_at"] is not None
        assert data["created_at"] == created_item["created_at"]

    def test_update_item_not_found(self, client):
        """Test updating non-existent item returns 404."""
        response = client.put(
            "/v1/items/999", json={"name": "Updated", "description": "Test"}
        )

        assert response.status_code == 404
        assert "detail" in response.json()


class TestItemDeletion:
    """Test cases for deleting items."""

    def test_delete_item_success(self, client, created_item):
        """Test successful item deletion."""
        item_id = created_item["id"]

        response = client.delete(f"/v1/items/{item_id}")

        assert response.status_code == 200
        assert "message" in response.json()

        # Verify item is deleted
        get_response = client.get(f"/v1/items/{item_id}")
        assert get_response.status_code == 404

    def test_delete_item_not_found(self, client):
        """Test deleting non-existent item returns 404."""
        response = client.delete("/v1/items/999")

        assert response.status_code == 404
        assert "detail" in response.json()


class TestHealthCheck:
    """Test cases for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestAPIVersioning:
    """Test cases for API versioning."""

    def test_v1_endpoints_work(self, client, sample_item_data):
        """Test that /v1/ prefixed endpoints work correctly."""
        # Create via v1
        v1_response = client.post("/v1/items", json=sample_item_data)
        assert v1_response.status_code == 200
        v1_data = v1_response.json()

        # Get via v1
        get_response = client.get(f"/v1/items/{v1_data['id']}")
        assert get_response.status_code == 200
        get_data = get_response.json()

        assert v1_data["id"] == get_data["id"]
        assert v1_data["name"] == get_data["name"]


class TestInputValidation:
    """Test cases for input validation."""

    def test_create_item_invalid_name_too_long(self, client):
        """Test creating item with name too long fails."""
        long_name = "a" * 101  # 101 characters, exceeds max_length=100
        response = client.post("/v1/items", json={"name": long_name})

        assert response.status_code == 422  # Validation error
        assert "name" in str(response.json())

    def test_create_item_invalid_name_empty(self, client):
        """Test creating item with empty name fails."""
        response = client.post("/v1/items", json={"name": ""})

        assert response.status_code == 422
        assert "name" in str(response.json())

    def test_create_item_invalid_description_too_long(self, client):
        """Test creating item with description too long fails."""
        long_desc = "a" * 501  # 501 characters, exceeds max_length=500
        response = client.post(
            "/v1/items", json={"name": "Valid Name", "description": long_desc}
        )

        assert response.status_code == 422
        assert "description" in str(response.json())

    def test_create_item_valid_minimal(self, client):
        """Test creating item with minimal valid data succeeds."""
        response = client.post("/v1/items", json={"name": "a"})  # Minimal valid name

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "a"
        assert data["description"] is None

    def test_update_item_invalid_data(self, client, created_item):
        """Test updating item with invalid data fails."""
        item_id = created_item["id"]
        response = client.put(
            f"/v1/items/{item_id}", json={"name": ""}
        )  # Invalid empty name

        assert response.status_code == 422
        assert "name" in str(response.json())
