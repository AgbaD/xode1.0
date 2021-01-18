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
    speech = db.Column(db.String(256))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))