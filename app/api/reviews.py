from flask import Blueprint, jsonify, request
from database import db
from app.models.product import Review, Product

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')


@reviews_bp.route('', methods=['GET'])
def list_reviews():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    product_id = request.args.get('product_id', type=int)
    sentiment = request.args.get('sentiment')
    min_rating = request.args.get('min_rating', type=int)

    query = Review.query

    if product_id:
        query = query.filter_by(product_id=product_id)
    if sentiment:
        query = query.filter_by(sentiment=sentiment)
    if min_rating:
        query = query.filter(Review.rating >= min_rating)

    pagination = query.order_by(Review.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'success': True,
        'data': {
            'reviews': [r.to_dict() for r in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
        }
    })


@reviews_bp.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify({'success': True, 'data': review.to_dict()})


@reviews_bp.route('', methods=['POST'])
def create_review():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    required = ['product_id', 'author_name', 'rating', 'content']
    for field in required:
        if not data.get(field):
            return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400

    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'success': False, 'error': 'Product not found'}), 404

    rating = int(data['rating'])
    if rating < 1 or rating > 5:
        return jsonify({'success': False, 'error': 'Rating must be 1-5'}), 400

    sentiment = 'positive' if rating >= 4 else ('negative' if rating <= 2 else 'neutral')
    sentiment_score = rating / 5.0

    review = Review(
        product_id=data['product_id'],
        author_name=data['author_name'],
        rating=rating,
        title=data.get('title', ''),
        content=data['content'],
        sentiment=sentiment,
        sentiment_score=sentiment_score,
        is_verified=data.get('is_verified', False),
    )
    db.session.add(review)

    product.review_count = Review.query.filter_by(product_id=product.product_id).count() + 1
    all_reviews = Review.query.filter_by(product_id=product.product_id).all()
    ratings = [r.rating for r in all_reviews] + [rating]
    product.avg_rating = sum(ratings) / len(ratings)

    db.session.commit()
    return jsonify({'success': True, 'data': review.to_dict()}), 201
