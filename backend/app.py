from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
import datetime
import requests

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/redbook'))
db = client.redbook

LOTR_API_BASE_URL = 'https://the-one-api.dev/v2'
LOTR_API_TOKEN = os.getenv('LOTR_API_TOKEN')

@app.route('/api/movies', methods=['GET'])
def search_movies():
    search_term = request.args.get('name', '')
    user_name = request.args.get('user', '')
    
    headers = {'Authorization': f'Bearer {LOTR_API_TOKEN}'}
    response = requests.get(f'{LOTR_API_BASE_URL}/movie', headers=headers)
    
    log_entry = {
        'user_name': user_name,
        'search_term': search_term,
        'timestamp': datetime.datetime.utcnow(),
        'results_count': 0
    }
    
    if response.status_code == 200:
        movies = response.json().get('docs', [])
        # Filter movies based on search term
        filtered_movies = [
            movie for movie in movies 
            if search_term.lower() in movie.get('name', '').lower()
        ]
        log_entry['results_count'] = len(filtered_movies)
        db.search_history.insert_one(log_entry)
        return jsonify({'movies': filtered_movies})
    
    return jsonify({'error': 'Failed to fetch movies'}), 500

@app.route('/api/history', methods=['GET'])
def get_search_history():
    history = list(db.search_history.find(
        {}, 
        {'_id': 0}
    ).sort('timestamp', -1))
    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)