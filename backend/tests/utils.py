# tests/utils.py

from functools import wraps
import time

def timing_decorator(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to execute")
        return result
    return wrapper

def assert_valid_movie(movie):
    """Helper function to validate movie object structure"""
    required_fields = {
        '_id': str,
        'name': str,
        'runtimeInMinutes': int,
        'budgetInMillions': (int, float),
        'boxOfficeRevenueInMillions': (int, float),
        'academyAwardNominations': int,
        'academyAwardWins': int
    }
    
    for field, expected_type in required_fields.items():
        assert field in movie, f"Missing required field: {field}"
        assert isinstance(movie[field], expected_type), \
            f"Field {field} has wrong type. Expected {expected_type}, got {type(movie[field])}"

def generate_test_movie(movie_id="test_id", name="Test Movie"):
    """Helper function to generate test movie data"""
    return {
        "_id": movie_id,
        "name": name,
        "runtimeInMinutes": 180,
        "budgetInMillions": 100,
        "boxOfficeRevenueInMillions": 1000,
        "academyAwardNominations": 10,
        "academyAwardWins": 5,
        "rottenTomatoesScore": 95
    }