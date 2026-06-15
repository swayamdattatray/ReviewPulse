from flask import Blueprint, jsonify, request
from sqlalchemy import func, extract
from database import db
from app.models.product import Product, Review

trends_bp = Blueprint('trends', __name__, url_prefix='/trends')


@trends_bp.route('/product/<int:product_id>', methods=['GET'])
def product_trends(product_id):
    product = Product.query.get_or_404(product_id)

    monthly = db.session.query(
        func.strftime('%Y-%m', Review.created_at).label('month'),
        func.avg(Review.rating).label('avg_rating'),
        func.count(Review.review_id).label('count'),
    ).filter_by(product_id=product_id).group_by('month').order_by('month').all()

    sentiment_over_time = db.session.query(
        func.strftime('%Y-%m', Review.created_at).label('month'),
        Review.sentiment,
        func.count(Review.review_id).label('count'),
    ).filter_by(product_id=product_id).group_by('month', 'sentiment').order_by('month').all()

    sentiment_data = {}
    for month, sentiment, count in sentiment_over_time:
        if month not in sentiment_data:
            sentiment_data[month] = {}
        sentiment_data[month][sentiment] = count

    return jsonify({
        'success': True,
        'data': {
            'product': product.to_dict(),
            'monthly_trends': [
                {'month': m, 'avg_rating': round(float(r), 2), 'review_count': c}
                for m, r, c in monthly
            ],
            'sentiment_trends': [
                {'month': m, **sentiment_data.get(m, {})}
                for m in sorted(set(row[0] for row in sentiment_over_time))
            ],
        }
    })


@trends_bp.route('/category', methods=['GET'])
def category_trends():
    category = request.args.get('category')
    query = db.session.query(
        Product.category,
        func.avg(Review.rating).label('avg_rating'),
        func.count(Review.review_id).label('review_count'),
        func.avg(Review.sentiment_score).label('avg_sentiment'),
    ).join(Review, Product.product_id == Review.product_id)

    if category:
        query = query.filter(Product.category == category)

    results = query.group_by(Product.category).all()

    return jsonify({
        'success': True,
        'data': [
            {
                'category': cat,
                'avg_rating': round(float(r), 2),
                'review_count': c,
                'avg_sentiment': round(float(s), 2),
            }
            for cat, r, c, s in results
        ]
    })
