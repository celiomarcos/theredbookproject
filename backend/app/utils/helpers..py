from datetime import datetime
import logging

def format_timestamp(timestamp):
    if isinstance(timestamp, str):
        return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return timestamp

def validate_movie_id(movie_id):
    # Add validation logic here
    return isinstance(movie_id, str) and len(movie_id) > 0