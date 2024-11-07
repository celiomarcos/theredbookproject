# app/routes/movie_routes.py
from flask import Blueprint, request, jsonify
from app.services.lotr_service import LotrService
from app.services.history_service import HistoryService

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/movies', methods=['GET'])
def get_movies():
    try:
        name = request.args.get('name', '')
        user_name = request.args.get('user', '')

        lotr_service = LotrService()
        history_service = HistoryService(movie_bp.current_app.db)

        # Get movies from LOTR API
        movies = lotr_service.get_movies(name)

        # Log the search
        if user_name:
            history_service.add_search(
                user_name=user_name,
                search_term=name,
                results_count=len(movies)
            )

        return jsonify({'movies': movies})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movie_bp.route('/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    try:
        lotr_service = LotrService()
        movie = lotr_service.get_movie_by_id(movie_id)
        
        if not movie:
            return jsonify({'error': 'Movie not found'}), 404
            
        return jsonify({'movie': movie})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# app/routes/history_routes.py
from flask import Blueprint, jsonify
from app.services.history_service import HistoryService

history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['GET'])
def get_history():
    try:
        history_service = HistoryService(history_bp.current_app.db)
        history = history_service.get_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500