# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/redbook')
    LOTR_API_TOKEN = os.getenv('LOTR_API_TOKEN')
    LOTR_API_BASE_URL = 'https://the-one-api.dev/v2'
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    TESTING = False

class TestConfig(Config):
    TESTING = True
    MONGODB_URI = 'mongodb://mongodb:27017/redbook_test'