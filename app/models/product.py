from datetime import datetime
from database import db


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    avg_rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    reviews = db.relationship('Review', backref='product', lazy=True)

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category,
            'brand': self.brand,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'avg_rating': self.avg_rating,
            'review_count': self.review_count,
            'created_at': self.created_at.isoformat(),
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    author_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), default='neutral')
    sentiment_score = db.Column(db.Float, default=0.0)
    is_verified = db.Column(db.Boolean, default=False)
    helpful_votes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'review_id': self.review_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'user_id': self.user_id,
            'author_name': self.author_name,
            'rating': self.rating,
            'title': self.title,
            'content': self.content,
            'sentiment': self.sentiment,
            'sentiment_score': self.sentiment_score,
            'is_verified': self.is_verified,
            'helpful_votes': self.helpful_votes,
            'created_at': self.created_at.isoformat(),
        }
