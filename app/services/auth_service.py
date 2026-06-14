from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime
from database import db
from app.models.user import User


def register_user():
    """
    Register a new user
    
    Request body:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "first_name": "string (optional)",
            "last_name": "string (optional)"
        }
    
    Returns:
        JSON with user data and status
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided',
                'code': 400
            }), 400
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'code': 400
                }), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        # Validate username
        if len(username) < 3:
            return jsonify({
                'success': False,
                'error': 'Username must be at least 3 characters',
                'code': 400
            }), 400
        
        if not is_valid_email(email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format',
                'code': 400
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 6 characters',
                'code': 400
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'error': 'Username already exists',
                'code': 409
            }), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'error': 'Email already registered',
                'code': 409
            }), 409
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='user'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        current_app.logger.info(f'New user registered: {username}')
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': user.to_dict(),
            },
            'code': 201
        }), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Registration error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Registration failed',
            'code': 500
        }), 500


def login_user():
    """
    Login user and return JWT tokens
    
    Request body:
        {
            "email": "string",
            "password": "string"
        }
    
    Returns:
        JSON with access token and user data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided',
                'code': 400
            }), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password required',
                'code': 400
            }), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password',
                'code': 401
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is inactive',
                'code': 403
            }), 403
        
        # Verify password
        if not user.check_password(password):
            return jsonify({
                'success': False,
                'error': 'Invalid email or password',
                'code': 401
            }), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create JWT tokens
        access_token = create_access_token(
            identity=user.user_id,
            additional_claims={'role': user.role}
        )
        refresh_token = create_refresh_token(identity=user.user_id)
        
        current_app.logger.info(f'User logged in: {user.username}')
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
            },
            'code': 200
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Login error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Login failed',
            'code': 500
        }), 500


@jwt_required()
def get_current_user():
    """
    Get current authenticated user
    
    Returns:
        JSON with user data
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found',
                'code': 404
            }), 404
        
        return jsonify({
            'success': True,
            'data': {'user': user.to_dict()},
            'code': 200
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Get user error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to get user',
            'code': 500
        }), 500


def is_valid_email(email):
    """
    Validate email format
    
    Args:
        email: Email address to validate
    
    Returns:
        Boolean indicating if email is valid
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
