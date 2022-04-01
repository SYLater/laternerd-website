from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Suggestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suggestion = db.Column(db.String(10000))
    email = db.Column(db.String(10000))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msgh = db.Column(db.String(10000))

