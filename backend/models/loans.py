from . import db


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_relationship = db.Column(
        db.Integer, db.ForeignKey('customer.id'), default=None)
    game_relationship = db.Column(
        db.Integer, db.ForeignKey('customer.id'), default=None)
