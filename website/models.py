from enum import unique
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, Unicode, update


from . import db


class Suggestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suggestion = db.Column(db.String(200))
    email = db.Column(db.String(200))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    UserName = db.Column(db.String(150))
    icon = db.Column(db.Text)
    paduaEmail = db.Column(db.String(150))
    paduaPassword = db.Column(db.String(150))
    classCodes = db.Column(db.String(9999))
    classNames = db.Column(db.String(9999))


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msgh = db.Column(db.String(200))
