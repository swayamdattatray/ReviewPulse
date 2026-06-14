from flask import Blueprint
from app.services.auth_service import register_user, login_user, get_current_user
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    POST /api/v1/auth/register
    
    Request body:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "first_name": "string (optional)",
            "last_name": "string (optional)"
        }
    
    Returns:
        201: User registered successfully
        400: Missing or invalid fields
        409: User already exists
    """
    return register_user()


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and get JWT tokens
    
    POST /api/v1/auth/login
    
    Request body:
        {
            "email": "string",
            "password": "string"
        }
    
    Returns:
        200: Login successful, returns access and refresh tokens
        400: Missing required fields
        401: Invalid credentials
    """
    return login_user()


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """
    Get current authenticated user
    
    GET /api/v1/auth/me
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: User data
        401: Unauthorized
        404: User not found
    """
    return get_current_user()
