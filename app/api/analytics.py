from flask import Blueprint, jsonify
from sqlalchemy import func
from database import db
from app.models.product import Product, Review

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')


@analytics_bp.route('/dashboard', methods=['GET'])
def dashboard():
    total_products = Product.query.count()
    total_reviews = Review.query.count()

    avg_rating = db.session.query(func.avg(Review.rating)).scalar() or 0

    sentiment_dist = db.session.query(
        Review.sentiment, func.count(Review.review_id)
    ).group_by(Review.sentiment).all()
    sentiment_counts = {s: c for s, c in sentiment_dist}

    rating_dist = db.session.query(
        Review.rating, func.count(Review.review_id)
    ).group_by(Review.rating).order_by(Review.rating).all()
    rating_counts = {str(r): c for r, c in rating_dist}

    top_products = Product.query.order_by(Product.avg_rating.desc()).limit(5).all()
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(5).all()

    verified_count = Review.query.filter_by(is_verified=True).count()
    verified_pct = (verified_count / total_reviews * 100) if total_reviews > 0 else 0

    return jsonify({
        'success': True,
        'data': {
            'summary': {
                'total_products': total_products,
                'total_reviews': total_reviews,
                'avg_rating': round(float(avg_rating), 2),
                'verified_pct': round(verified_pct, 1),
            },
            'sentiment_distribution': sentiment_counts,
            'rating_distribution': rating_counts,
            'top_products': [p.to_dict() for p in top_products],
            'recent_reviews': [r.to_dict() for r in recent_reviews],
        }
    })
