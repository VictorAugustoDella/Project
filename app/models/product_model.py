from app.db import db
from datetime import datetime

class Product(db.Model):
    __tablename__= 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product = db.Column(db.String, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_change = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    
    def to_dict(self):       
        return {    
            "id": self.id,
            "product": self.product,
            "added_at": self.added_at.isoformat(),
            "last_change": self.last_change.isoformat()
        }
