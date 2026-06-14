from flask import Blueprint, jsonify
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


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
            'auth': '/auth',
            'products': '/products',
            'reviews': '/reviews',
            'sentiment': '/sentiment',
            'fake_detection': '/fake-detection',
            'ai_detection': '/ai-detection',
            'trends': '/trends',
            'recommendations': '/recommendations',
            'analytics': '/analytics',
            'features': '/features',
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
        'endpoints': {
            'health': '/api/v1/health',
            'auth': '/api/v1/auth',
            'products': '/api/v1/products',
            'reviews': '/api/v1/reviews',
            'sentiment': '/api/v1/sentiment',
            'fake_detection': '/api/v1/fake-detection',
            'ai_detection': '/api/v1/ai-detection',
            'trends': '/api/v1/trends',
            'recommendations': '/api/v1/recommendations',
            'analytics': '/api/v1/analytics',
            'features': '/api/v1/features',
        },
        'features': [
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
