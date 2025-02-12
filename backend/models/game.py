from models import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    loan_status = db.Column(db.Boolean, nullable=False, default=False)  # אם המשחק מושאל
    customer_relationship = db.Column(
        db.Integer, db.ForeignKey('customer.id'), default=None)  # יכיל את מזהה הלקוח
