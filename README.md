# Quick Setup Guide

## 1. Prerequisites
- Docker and Docker Compose installed
- API token from [The One API](https://the-one-api.dev/)

## 2. Setup Steps

1. Clone repository:
```bash
git clone [repository-url]
cd redbook-project
```

2. Create `.env` file:
```env
LOTR_API_TOKEN=your_token_here
```

3. Run with Docker:
```bash
docker-compose up --build
```

4. Access application:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## 3. Local Development

### Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend:
```bash
cd frontend
npm install
npm start
```

## 4. Testing

### Backend Testing

The backend uses pytest for testing, with comprehensive test coverage for all endpoints and services.

#### Test Structure
```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configurations and fixtures
│   ├── test_movie_routes.py # Movie endpoint tests
│   ├── test_history_routes.py # History endpoint tests
│   └── utils.py             # Test utilities
├── pytest.ini               # Pytest configuration
└── requirements-test.txt    # Test dependencies
```

#### Setting Up Test Environment

1. Install test dependencies:
```bash
cd backend
pip install -r requirements-test.txt
```

2. Environment variables for testing:
```bash
export FLASK_ENV=testing
export MONGODB_URI=mongodb://localhost:27017/redbook_test
```

#### Running Tests

1. Run all tests:
```bash
pytest
```

2. Run specific test categories:
```bash
# Run only movie route tests
pytest tests/test_movie_routes.py

# Run only history route tests
pytest tests/test_history_routes.py

# Run tests with specific markers
pytest -m "benchmark"  # Performance tests
pytest -m "unit"      # Unit tests
pytest -m "api"       # API tests
```

3. Run tests with coverage report:
```bash
# Generate terminal and HTML coverage report
pytest --cov=app --cov-report=term-missing --cov-report=html

# View HTML coverage report
open htmlcov/index.html
```

4. Run tests in parallel:
```bash
pytest -n auto  # Uses all available CPU cores
```

#### Test Categories

- **Unit Tests**: Basic functionality tests
- **Integration Tests**: Tests involving multiple components
- **API Tests**: Full API endpoint testing
- **Performance Tests**: Response time and load testing
- **Security Tests**: Input validation and security measures

#### Available Test Markers

```python
@pytest.mark.benchmark  # Performance benchmarks
@pytest.mark.unit      # Unit tests
@pytest.mark.api       # API tests
@pytest.mark.security  # Security tests
@pytest.mark.integration  # Integration tests
```

#### Running Tests in Docker

1. Using docker-compose:
```bash
docker-compose run --rm backend pytest
```

2. With coverage:
```bash
docker-compose run --rm backend pytest --cov=app
```

### Frontend Testing

The frontend uses Jest and React Testing Library for component testing.

#### Running Frontend Tests

1. Run all tests:
```bash
cd frontend
npm test
```

2. Run tests with coverage:
```bash
npm test -- --coverage
```

3. Run specific test file:
```bash
npm test -- SearchPage.test.js
```

4. Watch mode:
```bash
npm test -- --watch
```

### End-to-End Testing

End-to-end testing is performed using Cypress.

1. Install Cypress:
```bash
cd frontend
npm install cypress --save-dev
```

2. Open Cypress Test Runner:
``
npx cypress open
```

3. Run Cypress tests headlessly:
```bash
npx cypress run
```

### Continuous Integration

The project includes GitHub Actions workflows for automated testing:

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      # Backend tests
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install backend dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run backend tests
        run: |
          cd backend
          pytest --cov=app
      
      # Frontend tests
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      - name: Install frontend dependencies
        run: |
          cd frontend
          npm install
      - name: Run frontend tests
        run: |
          cd frontend
          npm test -- --coverage
```

### Performance Testing

The project includes benchmark tests for critical operations:

```bash
# Run only benchmark tests
pytest -m benchmark

# Run with detailed statistics
pytest --benchmark-only --benchmark-histogram
```

### Test Coverage Goals

- Backend: Minimum 80% coverage
- Frontend: Minimum 70% coverage
- Critical paths: 100% coverage

### Troubleshooting Tests

Common issues and solutions:

1. MongoDB connection errors:
```bash
# Ensure MongoDB is running
docker-compose up -d mongodb

# Use test database
export MONGODB_URI=mongodb://localhost:27017/redbook_test
```

2. Test database cleanup:
```bash
# Reset test database
mongo redbook_test --eval "db.dropDatabase()"
```

3. Debugging tests:
```bash
# Run with detailed output
pytest -vv

# Debug with PDB
pytest --pdb

# Show local variables in tracebacks
pytest --showlocals
```

For more detailed information about testing specific components, refer to the documentation in the respective test files.

## 5. Common Issues

If you encounter issues:
1. Verify Docker is running
2. Check API token in .env
3. Ensure ports 3000 and 5000 are available
4. Verify MongoDB connection

For detailed information, ask celiomarcos@gmail.com. Thanks
