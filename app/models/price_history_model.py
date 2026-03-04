from app.db import db
from datetime import datetime

class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    collected_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    product = db.relationship(
    "Product",
    backref=db.backref('price_history', lazy=True,  cascade="all, delete-orphan")
    )
    
    def to_dict(self):       
        return {    
            "id": self.id,
            "product_id": self.product_id,
            "price": self.price,
            "collected_at": self.collected_at.isoformat()
        }