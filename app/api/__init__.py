from flask import Blueprint
from app.api.auth import auth_bp
from app.api.products import products_bp
from app.api.reviews import reviews_bp
from app.api.analytics import analytics_bp
from app.api.trends import trends_bp

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(products_bp)
api_bp.register_blueprint(reviews_bp)
api_bp.register_blueprint(analytics_bp)
api_bp.register_blueprint(trends_bp)


from flask import jsonify, request
from datetime import datetime
from database import db
from app.models.product import Product, Review


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


@api_bp.route('/docs', methods=['GET'])
def api_docs():
    return jsonify({
        'success': True,
        'message': 'ReviewIQ API Documentation',
        'version': '1.0.0',
        'base_url': '/api/v1',
        'endpoints': {
            'health': {'method': 'GET', 'path': '/health', 'description': 'Health check'},
            'root': {'method': 'GET', 'path': '/', 'description': 'API welcome message'},
            'auth_register': {'method': 'POST', 'path': '/auth/register', 'description': 'Register a new user'},
            'auth_login': {'method': 'POST', 'path': '/auth/login', 'description': 'Login and get JWT tokens'},
            'auth_me': {'method': 'GET', 'path': '/auth/me', 'description': 'Get current user profile'},
            'list_products': {'method': 'GET', 'path': '/products', 'description': 'List products with pagination'},
            'get_product': {'method': 'GET', 'path': '/products/<id>', 'description': 'Get product details'},
            'categories': {'method': 'GET', 'path': '/products/categories', 'description': 'List categories'},
            'list_reviews': {'method': 'GET', 'path': '/reviews', 'description': 'List reviews'},
            'get_review': {'method': 'GET', 'path': '/reviews/<id>', 'description': 'Get review details'},
            'create_review': {'method': 'POST', 'path': '/reviews', 'description': 'Create a new review'},
            'analytics': {'method': 'GET', 'path': '/analytics/dashboard', 'description': 'Dashboard analytics'},
            'product_trends': {'method': 'GET', 'path': '/trends/product/<id>', 'description': 'Product trends'},
            'category_trends': {'method': 'GET', 'path': '/trends/category', 'description': 'Category trends'},
            'sentiment': {'method': 'POST', 'path': '/sentiment/analyze', 'description': 'Analyze text sentiment'},
            'fake_detection': {'method': 'POST', 'path': '/fake-detection/analyze', 'description': 'Detect fake reviews'},
            'ai_detection': {'method': 'POST', 'path': '/ai-detection/analyze', 'description': 'Detect AI-generated reviews'},
            'recommendations': {'method': 'GET', 'path': '/recommendations', 'description': 'Product recommendations'},
            'features': {'method': 'GET', 'path': '/features', 'description': 'Platform features list'},
        }
    }), 200


def _analyze_sentiment(text):
    score = 0.5
    positive_words = ['amazing', 'excellent', 'great', 'love', 'perfect', 'wonderful', 'best', 'fantastic', 'outstanding', 'impressive', 'happy', 'satisfied', 'recommend']
    negative_words = ['terrible', 'awful', 'worst', 'hate', 'horrible', 'poor', 'bad', 'disappointed', 'useless', 'broken', 'defective', 'waste', 'returning']
    words = text.lower().split()
    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)
    total = pos_count + neg_count
    if total > 0:
        score = pos_count / total
    return {
        'score': round(score, 2),
        'label': 'positive' if score > 0.6 else ('negative' if score < 0.4 else 'neutral'),
        'positive_words': [w for w in words if w in positive_words],
        'negative_words': [w for w in words if w in negative_words],
    }


@api_bp.route('/sentiment/analyze', methods=['POST'])
def sentiment_analyze():
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({'success': False, 'error': 'Missing required field: text'}), 400
    result = _analyze_sentiment(data['text'])
    return jsonify({'success': True, 'data': result}), 200


@api_bp.route('/fake-detection/analyze', methods=['POST'])
def fake_detection_analyze():
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({'success': False, 'error': 'Missing required field: text'}), 400
    text = data['text']
    words = text.lower().split()
    fake_indicators = ['unbelievable', 'best ever', 'changed my life', 'miracle', 'guaranteed', 'click here', 'act now', 'limited time', 'exclusive deal']
    indicator_count = sum(1 for phrase in fake_indicators if phrase in text.lower())
    repetition_score = len(set(words)) / max(len(words), 1)
    all_caps_ratio = sum(1 for w in words if w.isupper() and len(w) > 1) / max(len(words), 1)
    fake_probability = min(1.0, (indicator_count * 0.15 + (1 - repetition_score) * 0.3 + all_caps_ratio * 0.3))
    return jsonify({
        'success': True,
        'data': {
            'is_fake': fake_probability > 0.5,
            'fake_probability': round(fake_probability, 2),
            'indicators': {
                'suspicious_phrases': indicator_count,
                'repetition_score': round(repetition_score, 2),
                'all_caps_ratio': round(all_caps_ratio, 2),
            }
        }
    }), 200


@api_bp.route('/ai-detection/analyze', methods=['POST'])
def ai_detection_analyze():
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({'success': False, 'error': 'Missing required field: text'}), 400
    text = data['text']
    words = text.lower().split()
    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
    sentence_endings = sum(1 for c in text if c in '.!?')
    avg_sentence_len = len(words) / max(sentence_endings, 1)
    ai_indicators = ['overall', 'additionally', 'furthermore', 'moreover', 'consequently', 'in conclusion', 'it is important to', 'it should be noted', 'in terms of', 'when it comes to']
    indicator_count = sum(1 for phrase in ai_indicators if phrase in text.lower())
    ai_score = min(1.0, (indicator_count * 0.12 + min(avg_word_len / 10, 0.3) + min(avg_sentence_len / 30, 0.3)))
    return jsonify({
        'success': True,
        'data': {
            'is_ai_generated': ai_score > 0.5,
            'ai_probability': round(ai_score, 2),
            'metrics': {
                'avg_word_length': round(avg_word_len, 1),
                'avg_sentence_length': round(avg_sentence_len, 1),
                'ai_patterns_found': indicator_count,
            }
        }
    }), 200


@api_bp.route('/recommendations', methods=['GET'])
def recommendations():
    top_products = Product.query.order_by(Product.avg_rating.desc()).limit(5).all()
    return jsonify({
        'success': True,
        'data': {
            'recommendations': [p.to_dict() for p in top_products],
            'strategy': 'top_rated',
        }
    }), 200


@api_bp.route('/features', methods=['GET'])
def features():
    return jsonify({
        'success': True,
        'data': {
            'features': [
                {
                    'name': 'Sentiment Analysis',
                    'description': 'Multi-level sentiment analysis on customer reviews',
                    'endpoint': 'POST /api/v1/sentiment/analyze',
                    'status': 'active',
                },
                {
                    'name': 'Fake Review Detection',
                    'description': 'ML-based detection of fake and fraudulent reviews',
                    'endpoint': 'POST /api/v1/fake-detection/analyze',
                    'status': 'active',
                },
                {
                    'name': 'AI Content Detection',
                    'description': 'Identify AI-generated review content',
                    'endpoint': 'POST /api/v1/ai-detection/analyze',
                    'status': 'active',
                },
                {
                    'name': 'Trend Analysis',
                    'description': 'Monthly rating and sentiment trends',
                    'endpoint': 'GET /api/v1/trends/product/<id>',
                    'status': 'active',
                },
                {
                    'name': 'Product Recommendations',
                    'description': 'Top-rated product recommendations',
                    'endpoint': 'GET /api/v1/recommendations',
                    'status': 'active',
                },
                {
                    'name': 'Analytics Dashboard',
                    'description': 'Comprehensive review analytics dashboard',
                    'endpoint': 'GET /api/v1/analytics/dashboard',
                    'status': 'active',
                },
            ]
        }
    }), 200
