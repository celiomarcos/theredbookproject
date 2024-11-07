# tests/conftest.py

import pytest
from app import create_app
from app.config import TestConfig
from datetime import datetime, timedelta
import mongomock

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app(TestConfig)
    # Use mongomock for testing
    app.db = mongomock.MongoClient().db
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers():
    """Authentication headers for protected routes"""
    return {'Authorization': 'Bearer test-token'}

@pytest.fixture
def mock_datetime(monkeypatch):
    """Mock datetime for consistent testing"""
    FAKE_TIME = datetime(2024, 1, 1, 12, 0, 0)
    class MockDateTime:
        @classmethod
        def utcnow(cls):
            return FAKE_TIME
    monkeypatch.setattr("app.models.search_history.datetime", MockDateTime)
    return FAKE_TIME