

from controller import db

class Commodity(db.Model):
    commodity_name = db.Column(db.Text, nullable = False)
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    quantity = db.Column(db.Integer)
    id1 = db.Column(db.Integer)
    q1 = db.Column(db.Integer)
    id2 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    id3 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
