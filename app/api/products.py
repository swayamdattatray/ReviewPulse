from flask import Blueprint, jsonify, request
from database import db
from app.models.product import Product, Review

products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('', methods=['GET'])
def list_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    search = request.args.get('search')

    query = Product.query

    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'success': True,
        'data': {
            'products': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
        }
    })


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).limit(10).all()

    data = product.to_dict()
    data['reviews'] = [r.to_dict() for r in reviews]
    return jsonify({'success': True, 'data': data})


@products_bp.route('/categories', methods=['GET'])
def list_categories():
    categories = db.session.query(Product.category).distinct().all()
    return jsonify({
        'success': True,
        'data': [c[0] for c in categories]
    })
