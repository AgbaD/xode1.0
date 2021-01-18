#!/usr/bin/python3
# Author:   @AgbaD | @agba_dr3

from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime


class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    current_speech = db.Column(db.String(256))
    previous_speech = db.Column(db.String(256))
    facebook = db.Column(db.String(64))
    twitter = db.Column(db.String(64))
    instagram = db.Column(db.String(64))


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    last_seen = db.Column(db.DateTime)
    most_recent_event_id = db.Column(db.Integer)
    # long&latt


class Handbook(db.Model, UserMixin):
    __tablename__ = "handbook"
    id = db.Column(db.Integer, primary_key=True)
    uploaded_on = db.Column(db.DateTime, default=datetime.utcnow())
    active = db.Column(db.Boolean, default=True)
    book = db.Column(db.String(128))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
