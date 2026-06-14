import os
import sys
from app import create_app, db
from database import init_db

app = create_app()


@app.before_request
def before_request():
    """Initialize database on first request if needed"""
    try:
        db.session.execute('SELECT 1')
    except Exception as e:
        app.logger.error(f'Database connection error: {e}')
        with app.app_context():
            init_db(app)


if __name__ == '__main__':
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    os.makedirs('models/pretrained', exist_ok=True)
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Initialize database
    with app.app_context():
        try:
            init_db(app)
            app.logger.info('Database initialized successfully')
        except Exception as e:
            app.logger.error(f'Failed to initialize database: {e}')
    
    # Run development server
    print('\n' + '='*60)
    print('ReviewIQ - AI-Powered Review Intelligence Platform')
    print('='*60)
    print('\nStarting Flask development server...')
    print('\nAPI Endpoints:')
    print('  - Health Check: http://localhost:5000/api/v1/health')
    print('  - API Root: http://localhost:5000/api/v1/')
    print('\nAccess the application at: http://localhost:5000')
    print('='*60 + '\n')
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
