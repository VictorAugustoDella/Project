from app.db import db
from datetime import datetime

class User(db.Model):
    __tablename__= 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_access = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):       
        return {    
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "last_access": self.last_access.isoformat() if self.last_access else None
        }