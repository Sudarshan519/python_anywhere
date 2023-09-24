
from flask_serialize import FlaskSerialize
from . import db
fs_mixin = FlaskSerialize(db)
class CarouselModel(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'logo': self.logo
        }
class MovieModel(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    movie=db.Column(db.String(255))
    trailer=db.Column(db.String(255))

class Tvshow(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    logo = db.Column(db.String(255)) 
    trailer=db.Column(db.String(255))
class Episode(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define a foreign key relationship to the User table
    tv_show_id = db.Column(db.Integer, db.ForeignKey('tvshow.id'), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    episode=db.Column(db.String(255))
    trailer=db.Column(db.String(255))

class SubscriponPlan(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)

class UserPlan(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id=db.Column(db.Integer,db.ForeignKey("payment.id"))
class Payment(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Float)
    type=db.Column(db.String(256))