import logging
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from app.config import Config
from app.routes.movie_routes import movie_bp
from app.routes.history_routes import history_bp

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize MongoDB
    client = MongoClient(app.config['MONGODB_URI'])
    app.db = client.get_default_database()
    
    # Register blueprints
    app.register_blueprint(movie_bp, url_prefix='/api')
    app.register_blueprint(history_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500

    return app