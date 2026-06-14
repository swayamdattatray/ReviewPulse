from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db


class User(db.Model):
    """User model for authentication and user management"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user', nullable=False)  # admin, analyst, user
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """
        Hash and set password
        
        Args:
            password: Plain text password
        """
        if not password or len(password) < 6:
            raise ValueError('Password must be at least 6 characters')
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify password against hash
        
        Args:
            password: Plain text password to verify
        
        Returns:
            Boolean indicating if password is correct
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert user to dictionary
        
        Returns:
            Dictionary representation of user
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }

    def __repr__(self):
        return f'<User {self.username}>'
