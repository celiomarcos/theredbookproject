# app/services/lotr_service.py
import requests
from flask import current_app
import logging

class LotrService:
    def __init__(self):
        self.base_url = current_app.config['LOTR_API_BASE_URL']
        self.headers = {
            'Authorization': f"Bearer {current_app.config['LOTR_API_TOKEN']}"
        }

    def get_movies(self, name=None):
        try:
            response = requests.get(
                f'{self.base_url}/movie',
                headers=self.headers
            )
            response.raise_for_status()
            
            movies = response.json().get('docs', [])
            
            if name:
                movies = [
                    movie for movie in movies
                    if name.lower() in movie.get('name', '').lower()
                ]
            
            return movies
        except requests.RequestException as e:
            logging.error(f"Error fetching movies: {str(e)}")
            raise

    def get_movie_by_id(self, movie_id):
        try:
            response = requests.get(
                f'{self.base_url}/movie/{movie_id}',
                headers=self.headers
            )
            response.raise_for_status()
            
            movies = response.json().get('docs', [])
            return movies[0] if movies else None
        except requests.RequestException as e:
            logging.error(f"Error fetching movie {movie_id}: {str(e)}")
            raise

# app/services/history_service.py
from app.models.search_history import SearchHistory

class HistoryService:
    def __init__(self, db):
        self.db = db

    def add_search(self, user_name, search_term, results_count):
        search = SearchHistory(user_name, search_term, results_count)
        self.db.search_history.insert_one(search.to_dict())
        return search

    def get_history(self):
        history = self.db.search_history.find().sort('timestamp', -1)
        return [SearchHistory.from_dict(h).to_dict() for h in history]