# tests/test_movie_routes.py

import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime

# Sample movie data that mimics LOTR API response
@pytest.fixture
def sample_movies():
    return {
        "docs": [
            {
                "_id": "5cd95395de30eff6ebccde5c",
                "name": "The Fellowship of the Ring",
                "runtimeInMinutes": 178,
                "budgetInMillions": 93,
                "boxOfficeRevenueInMillions": 897.7,
                "academyAwardNominations": 13,
                "academyAwardWins": 4,
                "rottenTomatoesScore": 91
            },
            {
                "_id": "5cd95395de30eff6ebccde5d",
                "name": "The Two Towers",
                "runtimeInMinutes": 179,
                "budgetInMillions": 94,
                "boxOfficeRevenueInMillions": 926.3,
                "academyAwardNominations": 6,
                "academyAwardWins": 2,
                "rottenTomatoesScore": 95
            }
        ],
        "total": 2,
        "limit": 1000,
        "offset": 0,
        "page": 1,
        "pages": 1
    }

@pytest.fixture
def mock_lotr_api(monkeypatch, sample_movies):
    """Mock LOTR API responses"""
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception("API Error")

    def mock_get(*args, **kwargs):
        if "movie" in args[0]:
            if len(args[0].split("/")) > 4:  # Specific movie endpoint
                movie_id = args[0].split("/")[-1]
                for movie in sample_movies["docs"]:
                    if movie["_id"] == movie_id:
                        return MockResponse({"docs": [movie]})
                return MockResponse({"docs": []}, 404)
            return MockResponse(sample_movies)
        return MockResponse({"error": "Not found"}, 404)

    monkeypatch.setattr("requests.get", mock_get)
    return mock_get

class TestMovieRoutes:
    """Test suite for movie-related routes"""

    def test_get_movies_no_params(self, client, mock_lotr_api):
        """Test getting all movies without search parameters"""
        response = client.get('/api/movies')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'movies' in data
        assert len(data['movies']) == 2
        assert data['movies'][0]['name'] == 'The Fellowship of the Ring'

    def test_get_movies_with_search(self, client, mock_lotr_api):
        """Test searching movies by name"""
        response = client.get('/api/movies?name=Tower')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['movies']) == 1
        assert 'Two Towers' in data['movies'][0]['name']

    def test_get_movies_with_user(self, client, mock_lotr_api):
        """Test searching movies with user tracking"""
        response = client.get('/api/movies?name=Ring&user=test_user')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify the search was logged in history
        history_response = client.get('/api/history')
        history_data = json.loads(history_response.data)
        
        assert any(
            entry['user_name'] == 'test_user' and 
            entry['search_term'] == 'Ring' 
            for entry in history_data['history']
        )

    def test_get_movie_by_id(self, client, mock_lotr_api):
        """Test getting a specific movie by ID"""
        movie_id = "5cd95395de30eff6ebccde5c"
        response = client.get(f'/api/movies/{movie_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'movie' in data
        assert data['movie']['_id'] == movie_id
        assert data['movie']['name'] == 'The Fellowship of the Ring'

    def test_get_movie_not_found(self, client, mock_lotr_api):
        """Test getting a non-existent movie"""
        response = client.get('/api/movies/nonexistent_id')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_movie_search_validation(self, client, mock_lotr_api):
        """Test movie search parameter validation"""
        # Test with very long search term
        long_search = 'a' * 1000
        response = client.get(f'/api/movies?name={long_search}')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    @patch('requests.get')
    def test_api_error_handling(self, mock_get, client):
        """Test handling of LOTR API errors"""
        # Simulate API error
        mock_get.side_effect = Exception("API Error")
        
        response = client.get('/api/movies')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data

    def test_search_history_integration(self, client, mock_lotr_api):
        """Test integration between movie search and history tracking"""
        # Perform multiple searches
        searches = [
            ('Ring', 'user1'),
            ('Tower', 'user1'),
            ('Hobbit', 'user2')
        ]
        
        for search_term, user in searches:
            client.get(f'/api/movies?name={search_term}&user={user}')

        # Check history
        response = client.get('/api/history')
        data = json.loads(response.data)
        
        assert len(data['history']) == len(searches)
        assert any(entry['user_name'] == 'user1' for entry in data['history'])
        assert any(entry['user_name'] == 'user2' for entry in data['history'])

    @pytest.mark.parametrize('invalid_input', [
        '"><script>alert(1)</script>',  # XSS attempt
        "'; DROP TABLE movies; --",     # SQL injection attempt
        '${system("ls")}',              # Command injection attempt
    ])
    def test_security_input_validation(self, client, mock_lotr_api, invalid_input):
        """Test handling of potentially malicious inputs"""
        response = client.get(f'/api/movies?name={invalid_input}')
        assert response.status_code in [200, 400]  # Should either sanitize or reject
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'movies' in data
            # Verify no injection occurred
            assert all('<script>' not in str(movie) for movie in data['movies'])

class TestMoviePerformance:
    """Performance tests for movie routes"""

    def test_movie_search_performance(self, client, mock_lotr_api, benchmark):
        """Benchmark movie search performance"""
        def search_movies():
            return client.get('/api/movies?name=Ring')
        
        result = benchmark(search_movies)
        assert result.status_code == 200

    @pytest.mark.parametrize('n_requests', [1, 10, 50])
    def test_concurrent_requests(self, client, mock_lotr_api, n_requests):
        """Test handling of concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return client.get('/api/movies')

        with concurrent.futures.ThreadPoolExecutor(max_workers=n_requests) as executor:
            futures = [executor.submit(make_request) for _ in range(n_requests)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        assert all(r.status_code == 200 for r in results)

class TestMovieRoutesIntegration:
    """Integration tests for movie routes"""

    def test_search_and_details_flow(self, client, mock_lotr_api):
        """Test the complete flow of searching and getting movie details"""
        # First search for movies
        search_response = client.get('/api/movies?name=Fellowship&user=test_user')
        assert search_response.status_code == 200
        search_data = json.loads(search_response.data)
        
        # Get first movie ID
        movie_id = search_data['movies'][0]['_id']
        
        # Get movie details
        details_response = client.get(f'/api/movies/{movie_id}')
        assert details_response.status_code == 200
        details_data = json.loads(details_response.data)
        
        # Verify details match search results
        assert search_data['movies'][0]['name'] == details_data['movie']['name']

    def test_error_formats(self, client, mock_lotr_api):
        """Test consistency of error response formats"""
        endpoints = [
            '/api/movies/invalid_id',
            '/api/movies?name=' + 'x' * 1000,
            '/api/movies?invalid_param=value'
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            data = json.loads(response.data)
            
            if response.status_code != 200:
                assert 'error' in data
                assert isinstance(data['error'], str)