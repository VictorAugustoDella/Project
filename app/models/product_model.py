from app.db import db
from datetime import datetime

class Product(db.Model):
    __tablename__= 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product = db.Column(db.String, nullable=False)
    scraped_name = db.Column(db.String, nullable=False)
    site = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_change = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    
    def to_dict(self):       
        return {    
            "id": self.id,
            "product": self.product,
            "scraped_name": self.scraped_name,
            "site": self.site,
            "url": self.url,
            "added_at": self.added_at.isoformat(),
            "last_change": self.last_change.isoformat()
        }
