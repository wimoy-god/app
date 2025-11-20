from app import db
from datetime import datetime

class Masterclass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructor = db.Column(db.String(120), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    seats = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Masterclass {self.title}>"
