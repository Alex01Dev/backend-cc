from config.db import db
from datetime import datetime

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('tbb_products.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('tbb_products')
