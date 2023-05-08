from app import db
from datetime import datetime

class Composer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birthday = db.Column(db.Date)
    compositions = db.relationship("Composition", back_populates="composer")

class Composition(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    opus_number = db.Column(db.Integer)
    movement_number = db.Column(db.Integer)
    title = db.Column(db.String)
    key_signature = db.Column(db.String)
    composer_id = db.Column(db.ForeignKey(Composer.id))
    url = db.Column(db.String)
    composer = db.relationship(Composer, lazy="joined", back_populates="compositions")
