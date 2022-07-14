import imp
from enum import unique

from flask_login import UserMixin
from sqlalchemy import (JSON, Column, ForeignKey, Integer, Table, Unicode,
                        update)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast

from . import db

# many to many
# user_history = db.Table('user_history',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('history.id', db.Integer, db.ForeignKey('history.id'))
#     )

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
    messages = db.relationship("History", backref="userid",)

class Padua(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    paduaEmail = db.Column(db.String(150))
    paduaName = db.Column(db.String(150))
    paduaPassword = db.Column(db.String(150))
    classCodes = db.Column(db.Text)
    classNames = db.Column(db.Text)
    classDomain = db.Column(db.Text)
    Grades = db.Column(db.Text)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    msg = db.Column(db.String(200))
    Timestamp = db.Column(db.String(150))



