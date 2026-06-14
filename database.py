from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool

db = SQLAlchemy()


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()


def reset_db(app):
    """Reset database - use with caution"""
    with app.app_context():
        db.drop_all()
        db.create_all()
