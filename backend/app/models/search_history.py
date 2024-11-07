# app/models/search_history.py
from datetime import datetime

class SearchHistory:
    def __init__(self, user_name, search_term, results_count):
        self.user_name = user_name
        self.search_term = search_term
        self.results_count = results_count
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            'user_name': self.user_name,
            'search_term': self.search_term,
            'results_count': self.results_count,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(data):
        search = SearchHistory(
            user_name=data['user_name'],
            search_term=data['search_term'],
            results_count=data['results_count']
        )
        search.timestamp = data.get('timestamp', datetime.utcnow())
        return search