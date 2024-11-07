# run.py
from app import create_app, setup_logger

logger = setup_logger()
app = create_app()

if __name__ == '__main__':
    logger.info('Starting The Red Book Project backend server...')
    app.run(host='0.0.0.0', port=5000)