import random
from datetime import datetime, timedelta
from database import db
from app.models.user import User
from app.models.product import Product, Review

PRODUCTS = [
    {"name": "Sony WH-1000XM5 Headphones", "category": "Electronics", "brand": "Sony", "price": 348.00, "description": "Industry-leading noise canceling headphones with exceptional sound quality."},
    {"name": "Apple MacBook Pro 14\"", "category": "Electronics", "brand": "Apple", "price": 1999.00, "description": "M3 Pro chip, 18GB RAM, 512GB SSD laptop."},
    {"name": "Samsung Galaxy S24 Ultra", "category": "Electronics", "brand": "Samsung", "price": 1299.99, "description": "旗舰 smartphone with AI-powered camera and S Pen."},
    {"name": "Dyson V15 Detect", "category": "Home", "brand": "Dyson", "price": 749.99, "description": "Cordless vacuum with laser dust detection."},
    {"name": "Kindle Paperwhite", "category": "Electronics", "brand": "Amazon", "price": 139.99, "description": "6.8\" display e-reader with adjustable warm light."},
    {"name": "Nike Air Max 270", "category": "Fashion", "brand": "Nike", "price": 150.00, "description": "Men's running shoes with Max Air unit."},
    {"name": "Instant Pot Duo 7-in-1", "category": "Home", "brand": "Instant Pot", "price": 89.95, "description": "Electric pressure cooker, 6 quart capacity."},
    {"name": "Bose QuietComfort Earbuds", "category": "Electronics", "brand": "Bose", "price": 249.00, "description": "True wireless noise cancelling earbuds."},
    {"name": "Le Creuset Dutch Oven", "category": "Home", "brand": "Le Creuset", "price": 379.95, "description": "5.5 qt round cast iron Dutch oven."},
    {"name": "Adidas Ultraboost", "category": "Fashion", "brand": "Adidas", "price": 190.00, "description": "Running shoes with responsive Boost cushioning."},
    {"name": "Logitech MX Master 3S", "category": "Electronics", "brand": "Logitech", "price": 99.99, "description": "Wireless ergonomic mouse with quiet clicks."},
    {"name": "All-Clad Stainless Cookware Set", "category": "Home", "brand": "All-Clad", "price": 699.95, "description": "10-piece tri-ply stainless steel cookware set."},
]

AUTHOR_NAMES = [
    "Alex M.", "Jordan K.", "Sam P.", "Casey R.", "Morgan T.",
    "Riley B.", "Quinn L.", "Avery S.", "Taylor W.", "Drew F.",
    "Jamie H.", "Dakota N.", "Reese C.", "Skyler D.", "Peyton G.",
    "Charlie V.", "Finley A.", "Harper J.", "Emerson Z.", "Rowan E.",
]

REVIEW_TEMPLATES = {
    5: [
        "Absolutely love this product! Exceeded all my expectations.",
        "Best purchase I've made this year. Highly recommend!",
        "Perfect in every way. Worth every penny.",
        "Outstanding quality and performance. 10/10.",
        "This is exactly what I was looking for. Amazing!",
    ],
    4: [
        "Great product overall. Minor issues but very satisfied.",
        "Really good quality for the price. Would recommend.",
        "Impressed with the performance. Just a few small gripes.",
        "Solid product that does what it promises.",
        "Very happy with this purchase. Does everything well.",
    ],
    3: [
        "Decent product but nothing special. Gets the job done.",
        "Average quality. Some features are great, others lacking.",
        "It's okay. Not bad but not amazing either.",
        "Mixed feelings. Some aspects are good, others need work.",
        "Meets basic expectations but doesn't stand out.",
    ],
    2: [
        "Disappointed with the quality. Expected better.",
        "Not great. Has some significant issues.",
        "Below average. Would not recommend at this price.",
        "Struggles with basic tasks. Frustrating experience.",
        "Had high hopes but let down. Needs improvement.",
    ],
    1: [
        "Terrible product. Broke within a week.",
        "Worst purchase ever. Complete waste of money.",
        "Doesn't work as advertised. Very disappointed.",
        "Absolutely awful. Returning immediately.",
        "Save your money. This product is garbage.",
    ],
}


def seed_database(app):
    with app.app_context():
        if Product.query.first():
            print("Database already seeded.")
            return

        admin = User(username="admin", email="admin@reviewiq.com", first_name="Admin", last_name="User", role="admin")
        admin.set_password("admin123")
        analyst = User(username="analyst", email="analyst@reviewiq.com", first_name="Data", last_name="Analyst", role="analyst")
        analyst.set_password("analyst123")
        demo = User(username="demo", email="demo@reviewiq.com", first_name="Demo", last_name="User", role="user")
        demo.set_password("demo123")
        db.session.add_all([admin, analyst, demo])
        db.session.flush()

        products = []
        for p in PRODUCTS:
            product = Product(**p)
            db.session.add(product)
            products.append(product)
        db.session.flush()

        sentiments = ['positive', 'neutral', 'negative']
        now = datetime.utcnow()

        for product in products:
            num_reviews = random.randint(8, 25)
            for _ in range(num_reviews):
                rating = random.choices([5, 4, 3, 2, 1], weights=[30, 35, 20, 10, 5])[0]
                sentiment = 'positive' if rating >= 4 else ('negative' if rating <= 2 else 'neutral')
                days_ago = random.randint(0, 365)
                review = Review(
                    product_id=product.product_id,
                    author_name=random.choice(AUTHOR_NAMES),
                    rating=rating,
                    title=f"Review for {product.name}",
                    content=random.choice(REVIEW_TEMPLATES[rating]),
                    sentiment=sentiment,
                    sentiment_score=rating / 5.0,
                    is_verified=random.random() > 0.3,
                    helpful_votes=random.randint(0, 50),
                    created_at=now - timedelta(days=days_ago, hours=random.randint(0, 23)),
                )
                db.session.add(review)

        db.session.flush()

        for product in products:
            reviews = Review.query.filter_by(product_id=product.product_id).all()
            product.review_count = len(reviews)
            product.avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0

        db.session.commit()
        print(f"Seeded {len(products)} products and {Review.query.count()} reviews.")
