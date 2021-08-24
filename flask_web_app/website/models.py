from . import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200)) #unique - len jeden moze byt rovnaky
    password = db.Column(db.String(20))
    finger_id = db.Column(db.Integer)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    log_password = db.Column(db.Integer)
    rights = db.Column(db.String(20))
    reservation = db.relationship('Reservation', lazy='subquery')
    

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=False))    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
