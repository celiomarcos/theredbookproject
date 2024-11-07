# app/routes/history_routes.py
from flask import Blueprint, jsonify, request, current_app
from app.services.history_service import HistoryService
from datetime import datetime, timedelta
import logging

# Initialize blueprint and logger
history_bp = Blueprint('history', __name__)
logger = logging.getLogger(__name__)

@history_bp.route('/history', methods=['GET'])
def get_history():
    """
    Get search history with filtering, sorting, and pagination.
    Query parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    - sort: Sort field (timestamp, user_name, search_term, results_count)
    - order: Sort order (asc, desc)
    - user: Filter by username
    - date_from: Filter by date (YYYY-MM-DD)
    - date_to: Filter by date (YYYY-MM-DD)
    - search: Search in user_name or search_term
    """
    try:
        # Get query parameters with defaults
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        sort_field = request.args.get('sort', 'timestamp')
        sort_order = request.args.get('order', 'desc')
        user_filter = request.args.get('user', None)
        date_from = request.args.get('date_from', None)
        date_to = request.args.get('date_to', None)
        search = request.args.get('search', None)

        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10

        # Build filter query
        query = {}
        
        if user_filter:
            query['user_name'] = {'$regex': user_filter, '$options': 'i'}

        if search:
            query['$or'] = [
                {'user_name': {'$regex': search, '$options': 'i'}},
                {'search_term': {'$regex': search, '$options': 'i'}}
            ]

        # Date filtering
        if date_from or date_to:
            query['timestamp'] = {}
            if date_from:
                try:
                    from_date = datetime.strptime(date_from, '%Y-%m-%d')
                    query['timestamp']['$gte'] = from_date
                except ValueError:
                    return jsonify({'error': 'Invalid date_from format. Use YYYY-MM-DD'}), 400

            if date_to:
                try:
                    to_date = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
                    query['timestamp']['$lt'] = to_date
                except ValueError:
                    return jsonify({'error': 'Invalid date_to format. Use YYYY-MM-DD'}), 400

        # Validate sort field
        valid_sort_fields = ['timestamp', 'user_name', 'search_term', 'results_count']
        if sort_field not in valid_sort_fields:
            sort_field = 'timestamp'

        # Validate sort order
        sort_direction = -1 if sort_order.lower() == 'desc' else 1

        try:
            # Initialize history service
            history_service = HistoryService(current_app.db)
            
            # Get paginated results
            total_count = history_service.count_history(query)
            history_items = history_service.get_history_paginated(
                query=query,
                page=page,
                per_page=per_page,
                sort_field=sort_field,
                sort_direction=sort_direction
            )

            # Calculate pagination metadata
            total_pages = (total_count + per_page - 1) // per_page
            has_next = page < total_pages
            has_prev = page > 1

            # Prepare response
            response = {
                'history': history_items,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total_items': total_count,
                    'total_pages': total_pages,
                    'has_next': has_next,
                    'has_prev': has_prev
                },
                'filters': {
                    'user': user_filter,
                    'date_from': date_from,
                    'date_to': date_to,
                    'search': search
                },
                'sort': {
                    'field': sort_field,
                    'order': sort_order
                }
            }

            return jsonify(response)

        except Exception as e:
            logger.error(f"Database error in get_history: {str(e)}")
            return jsonify({'error': 'Database error occurred'}), 500

    except ValueError as e:
        logger.error(f"Invalid parameter in get_history: {str(e)}")
        return jsonify({'error': 'Invalid parameters provided'}), 400
    except Exception as e:
        logger.error(f"Unexpected error in get_history: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@history_bp.route('/history/stats', methods=['GET'])
def get_history_stats():
    """
    Get statistics about search history.
    Returns counts of searches by day, popular search terms, and active users.
    """
    try:
        history_service = HistoryService(current_app.db)
        
        # Get date range for stats
        days = int(request.args.get('days', 7))
        if days < 1 or days > 30:
            days = 7

        stats = history_service.get_statistics(days)
        return jsonify(stats)

    except Exception as e:
        logger.error(f"Error getting history stats: {str(e)}")
        return jsonify({'error': 'Error retrieving statistics'}), 500

@history_bp.route('/history/<user_name>', methods=['GET'])
def get_user_history(user_name):
    """
    Get search history for a specific user.
    """
    try:
        history_service = HistoryService(current_app.db)
        user_history = history_service.get_user_history(user_name)
        
        if not user_history:
            return jsonify({'message': 'No history found for this user'}), 404
            
        return jsonify({'history': user_history})

    except Exception as e:
        logger.error(f"Error getting user history: {str(e)}")
        return jsonify({'error': 'Error retrieving user history'}), 500

@history_bp.route('/history/clear', methods=['POST'])
def clear_history():
    """
    Clear search history. Optionally filter by user or date range.
    Requires confirmation in request body.
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.get_json()
        if not data.get('confirm', False):
            return jsonify({'error': 'Confirmation required'}), 400

        user_name = data.get('user_name')
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        history_service = HistoryService(current_app.db)
        deleted_count = history_service.clear_history(user_name, date_from, date_to)

        return jsonify({
            'message': 'History cleared successfully',
            'deleted_count': deleted_count
        })

    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        return jsonify({'error': 'Error clearing history'}), 500