import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import get_config
from database import db, init_db


def create_app(config=None):
    """
    Application factory for creating Flask app
    
    Args:
        config: Configuration class to use
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt = JWTManager(app)
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('models/pretrained', exist_ok=True)
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Setup logging
    setup_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    # Context processors
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}
    
    return app


def setup_logging(app):
    """
    Setup application logging
    
    Args:
        app: Flask application instance
    """
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            )
        )
        file_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(file_handler)
        app.logger.setLevel(app.config['LOG_LEVEL'])
        app.logger.info('ReviewIQ startup')


def register_error_handlers(app):
    """
    Register error handlers
    
    Args:
        app: Flask application instance
    """
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'code': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'code': 500
        }), 500
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'success': False,
            'error': 'Bad request',
            'code': 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'code': 401
        }), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'code': 403
        }), 403


def register_blueprints(app):
    """
    Register API blueprints
    
    Args:
        app: Flask application instance
    """
    from app.api import api_bp
    app.register_blueprint(api_bp)


def register_cli_commands(app):
    """
    Register CLI commands
    
    Args:
        app: Flask application instance
    """
    @app.cli.command()
    def init_db_command():
        """Initialize the database."""
        init_db(app)
        print('Database initialized.')
    
    @app.cli.command()
    def drop_db_command():
        """Drop all database tables."""
        if input('Are you sure you want to drop all tables? (yes/no): ').lower() == 'yes':
            db.drop_all()
            print('Database dropped.')
        else:
            print('Operation cancelled.')
    
    @app.cli.command()
    def seed_db_command():
        """Seed database with sample data."""
        from app.utils.seed import seed_database
        seed_database(app)
        print('Database seeded with sample data.')
