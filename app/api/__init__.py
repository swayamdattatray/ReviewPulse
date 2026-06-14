from flask import Blueprint
from app.api.auth import auth_bp

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Register auth blueprint
api_bp.register_blueprint(auth_bp)


from flask import jsonify
from datetime import datetime


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON with health status and timestamp
    """
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'ReviewIQ API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'auth': {
                'register': 'POST /api/v1/auth/register',
                'login': 'POST /api/v1/auth/login',
                'me': 'GET /api/v1/auth/me',
            },
            'products': 'GET /api/v1/products',
            'reviews': 'GET /api/v1/reviews',
            'sentiment': 'POST /api/v1/sentiment/analyze',
            'fake_detection': 'POST /api/v1/fake-detection/analyze',
            'ai_detection': 'POST /api/v1/ai-detection/analyze',
            'trends': 'GET /api/v1/trends',
            'recommendations': 'GET /api/v1/recommendations',
            'analytics': 'GET /api/v1/analytics/dashboard',
            'features': 'GET /api/v1/features',
        }
    }), 200


@api_bp.route('/', methods=['GET'])
def api_root():
    """
    API root endpoint with welcome message
    
    Returns:
        JSON with API information
    """
    return jsonify({
        'success': True,
        'message': 'Welcome to ReviewIQ API',
        'description': 'AI-Powered Customer Review Intelligence Platform',
        'version': '1.0.0',
        'documentation': '/api/v1/docs',
        'quick_start': {
            'register': 'POST /api/v1/auth/register',
            'login': 'POST /api/v1/auth/login',
            'get_profile': 'GET /api/v1/auth/me',
        },
        'features': [
            'User authentication with JWT',
            'Multi-level sentiment analysis',
            'Fake review detection',
            'AI-generated review detection',
            'Feature-level sentiment analysis',
            'Trend analysis and forecasting',
            'Product recommendations',
            'Review summarization',
            'Advanced analytics',
        ]
    }), 200
