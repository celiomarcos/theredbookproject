# app/services/history_service.py
from datetime import datetime, timedelta
from app.models.search_history import SearchHistory

class HistoryService:
    def __init__(self, db):
        self.db = db
        self.collection = db.search_history

    def add_search(self, user_name, search_term, results_count):
        """Add a new search to history"""
        search = SearchHistory(user_name, search_term, results_count)
        self.collection.insert_one(search.to_dict())
        return search

    def get_history_paginated(self, query=None, page=1, per_page=10, 
                            sort_field='timestamp', sort_direction=-1):
        """Get paginated search history with filters and sorting"""
        if query is None:
            query = {}

        skip = (page - 1) * per_page
        cursor = self.collection.find(
            query,
            {'_id': 0}  # Exclude MongoDB _id
        ).sort(
            sort_field, sort_direction
        ).skip(skip).limit(per_page)

        return list(cursor)

    def count_history(self, query=None):
        """Count total history entries matching query"""
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    def get_user_history(self, user_name):
        """Get all search history for a specific user"""
        cursor = self.collection.find(
            {'user_name': user_name},
            {'_id': 0}
        ).sort('timestamp', -1)
        return list(cursor)

    def get_statistics(self, days=7):
        """Get search history statistics"""
        date_limit = datetime.utcnow() - timedelta(days=days)
        
        # Daily searches
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': date_limit}
                }
            },
            {
                '$group': {
                    '_id': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$timestamp'
                        }
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'_id': 1}
            }
        ]
        daily_searches = list(self.collection.aggregate(pipeline))

        # Popular search terms
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': date_limit},
                    'search_term': {'$ne': ''}
                }
            },
            {
                '$group': {
                    '_id': '$search_term',
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'count': -1}
            },
            {
                '$limit': 10
            }
        ]
        popular_terms = list(self.collection.aggregate(pipeline))

        # Active users
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': date_limit}
                }
            },
            {
                '$group': {
                    '_id': '$user_name',
                    'search_count': {'$sum': 1},
                    'last_search': {'$max': '$timestamp'}
                }
            },
            {
                '$sort': {'search_count': -1}
            },
            {
                '$limit': 10
            }
        ]
        active_users = list(self.collection.aggregate(pipeline))

        return {
            'daily_searches': daily_searches,
            'popular_terms': popular_terms,
            'active_users': active_users,
            'period_days': days,
            'total_searches': self.count_history({'timestamp': {'$gte': date_limit}})
        }

    def clear_history(self, user_name=None, date_from=None, date_to=None):
        """Clear search history with optional filters"""
        query = {}
        
        if user_name:
            query['user_name'] = user_name
            
        if date_from or date_to:
            query['timestamp'] = {}
            if date_from:
                query['timestamp']['$gte'] = datetime.strptime(date_from, '%Y-%m-%d')
            if date_to:
                query['timestamp']['$lt'] = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)

        result = self.collection.delete_many(query)
        return result.deleted_count