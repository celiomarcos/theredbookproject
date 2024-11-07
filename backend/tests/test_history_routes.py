# tests/test_history_routes.py

import pytest
from datetime import datetime, timedelta
import json
from bson import json_util

@pytest.fixture
def sample_history_data():
    """Fixture to provide sample history data"""
    return [
        {
            "user_name": "john_doe",
            "search_term": "Lord of the Rings",
            "results_count": 3,
            "timestamp": datetime.utcnow() - timedelta(days=1)
        },
        {
            "user_name": "jane_doe",
            "search_term": "The Hobbit",
            "results_count": 2,
            "timestamp": datetime.utcnow() - timedelta(days=2)
        },
        {
            "user_name": "john_doe",
            "search_term": "Return of the King",
            "results_count": 1,
            "timestamp": datetime.utcnow() - timedelta(days=3)
        }
    ]

@pytest.fixture
def setup_test_data(app, sample_history_data):
    """Fixture to set up test data in the database"""
    with app.app_context():
        # Clear existing data
        app.db.search_history.delete_many({})
        # Insert sample data
        app.db.search_history.insert_many(sample_history_data)
    yield
    with app.app_context():
        app.db.search_history.delete_many({})

class TestHistoryRoutes:
    """Test suite for history routes"""

    def test_get_history_basic(self, client, setup_test_data):
        """Test basic history retrieval"""
        response = client.get('/api/history')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'history' in data
        assert 'pagination' in data
        assert len(data['history']) == 3
        assert data['pagination']['total_items'] == 3

    def test_get_history_pagination(self, client, setup_test_data):
        """Test history pagination"""
        # Test first page with 2 items per page
        response = client.get('/api/history?page=1&per_page=2')
        data = json.loads(response.data)
        
        assert len(data['history']) == 2
        assert data['pagination']['page'] == 1
        assert data['pagination']['has_next'] == True
        assert data['pagination']['has_prev'] == False

        # Test second page
        response = client.get('/api/history?page=2&per_page=2')
        data = json.loads(response.data)
        
        assert len(data['history']) == 1
        assert data['pagination']['page'] == 2
        assert data['pagination']['has_next'] == False
        assert data['pagination']['has_prev'] == True

    def test_get_history_sorting(self, client, setup_test_data):
        """Test history sorting"""
        # Test sorting by user_name ascending
        response = client.get('/api/history?sort=user_name&order=asc')
        data = json.loads(response.data)
        
        users = [item['user_name'] for item in data['history']]
        assert users == sorted(users)

        # Test sorting by timestamp descending
        response = client.get('/api/history?sort=timestamp&order=desc')
        data = json.loads(response.data)
        
        timestamps = [item['timestamp'] for item in data['history']]
        assert timestamps == sorted(timestamps, reverse=True)

    def test_get_history_filtering(self, client, setup_test_data):
        """Test history filtering"""
        # Test filtering by user
        response = client.get('/api/history?user=john_doe')
        data = json.loads(response.data)
        
        assert all(item['user_name'] == 'john_doe' for item in data['history'])
        assert len(data['history']) == 2

        # Test filtering by search term
        response = client.get('/api/history?search=Hobbit')
        data = json.loads(response.data)
        
        assert len(data['history']) == 1
        assert data['history'][0]['search_term'] == 'The Hobbit'

    def test_get_history_date_range(self, client, setup_test_data):
        """Test history date range filtering"""
        date_from = (datetime.utcnow() - timedelta(days=2)).strftime('%Y-%m-%d')
        date_to = datetime.utcnow().strftime('%Y-%m-%d')
        
        response = client.get(f'/api/history?date_from={date_from}&date_to={date_to}')
        data = json.loads(response.data)
        
        assert len(data['history']) == 2

    def test_get_history_invalid_params(self, client, setup_test_data):
        """Test history with invalid parameters"""
        # Test invalid page number
        response = client.get('/api/history?page=0')
        assert response.status_code == 200  # Should default to page 1
        
        # Test invalid per_page
        response = client.get('/api/history?per_page=1000')
        data = json.loads(response.data)
        assert data['pagination']['per_page'] == 10  # Should default to 10

        # Test invalid date format
        response = client.get('/api/history?date_from=invalid-date')
        assert response.status_code == 400

    def test_get_user_history(self, client, setup_test_data):
        """Test getting history for specific user"""
        response = client.get('/api/history/john_doe')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert all(item['user_name'] == 'john_doe' for item in data['history'])

    def test_get_history_stats(self, client, setup_test_data):
        """Test getting history statistics"""
        response = client.get('/api/history/stats')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert 'daily_searches' in data
        assert 'popular_terms' in data
        assert 'active_users' in data
        assert 'total_searches' in data

    def test_clear_history(self, client, setup_test_data):
        """Test clearing history"""
        # Test without confirmation
        response = client.post('/api/history/clear',
                             json={'confirm': False})
        assert response.status_code == 400

        # Test with confirmation
        response = client.post('/api/history/clear',
                             json={'confirm': True})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['deleted_count'] == 3

        # Verify history is cleared
        response = client.get('/api/history')
        data = json.loads(response.data)
        assert len(data['history']) == 0

    def test_clear_history_with_filters(self, client, setup_test_data):
        """Test clearing history with filters"""
        response = client.post('/api/history/clear',
                             json={
                                 'confirm': True,
                                 'user_name': 'john_doe'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['deleted_count'] == 2

        # Verify only john_doe's history is cleared
        response = client.get('/api/history')
        data = json.loads(response.data)
        assert len(data['history']) == 1
        assert data['history'][0]['user_name'] == 'jane_doe'

class TestHistoryRoutesError:
    """Test suite for error handling in history routes"""

    def test_database_error(self, client, monkeypatch):
        """Test handling of database errors"""
        def mock_find(*args, **kwargs):
            raise Exception("Database error")

        monkeypatch.setattr("pymongo.collection.Collection.find", mock_find)
        response = client.get('/api/history')
        assert response.status_code == 500
        assert b'Database error occurred' in response.data

    @pytest.mark.parametrize('endpoint,method', [
        ('/api/history', 'GET'),
        ('/api/history/stats', 'GET'),
        ('/api/history/clear', 'POST')
    ])
    def test_error_handling(self, client, endpoint, method):
        """Test general error handling for all endpoints"""
        if method == 'GET':
            response = client.get(endpoint + '?invalid=parameter')
        else:
            response = client.post(endpoint, json={'invalid': 'data'})
            
        assert response.status_code in [400, 500]
        assert 'error' in json.loads(response.data)

def test_history_performance(client, setup_test_data, benchmark):
    """Test performance of history retrieval"""
    def get_history():
        return client.get('/api/history')
    
    result = benchmark(get_history)
    assert result.status_code == 200