#!/bin/bash
# setup_tests.sh

# Create necessary directories
mkdir -p backend/tests/coverage

# Install test dependencies
pip install -r requirements-test.txt

# Create initial test database
python -c "
from app import create_app
from app.config import TestConfig
app = create_app(TestConfig)
with app.app_context():
    db = app.db
    db.command('dropDatabase')
"

# Run tests with coverage
pytest --cov=app --cov-report=html:tests/coverage