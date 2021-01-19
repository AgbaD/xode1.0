#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

# packages
from flask import *
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

# user created
from . import main
from .. import db
from ..models import Admin, Userlogs, Handbook
from ..schema import validate_login

# inbuilt
from datetime import datetime


@main.route("/login", methods=['GET', 'POSt'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me")

        data = {"email": email, "password": password}
        # check schema
        schema_val = validate_login(data)
        if schema_val["msg"] != "success":
            flash(schema_val["error"])
            return render_template('login.html', data=data)

        user = Admin.query.filter_by(email=email).first()
        if not user:
            flash("Account not found please check email.")
            return render_template("login.html", data=data)
        if not check_password_hash(user.password_hash, password):
            flash("Password incorrect!")
            return render_template("login.html", data=data)

        login_user(user, remember_me)
        return redirect(url_for("main.dash"))
    return render_template('login.html')


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# Authentication Done


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Error Handler Done


@main.route("/dash")
@login_required
def dash():
    return render_template("dash.html", user=current_user)


@main.route("/socials", methods=["GET", "POST"])
@login_required
def socials():
    if request.method == "POST":
        if request.form.get("facebook"):
            current_user.facebook = request.form.get("facebook")
        if request.form.get("twitter"):
            current_user.twitter = request.form.get("twitter")
        if request.form.get("instagram"):
            current_user.instagram = request.form.get("instagram")

        db.session.add()
        db.session.commit()

    fb = current_user.facebook
    tw = current_user.twitter
    ig = current_user.instagram
    social = {"fb": fb, "tw": tw, "ig": ig}
    return render_template(socials.html, data=social)


@main.route("/speech", methods=["GET", "POST"])
@login_required
def speech():
    if request.method == "POST":
        speech_now = request.form.get("speech")
        cur = current_user.current_speech
        current_user.previous_speech = cur
        current_user.current_speech = speech_now

        db.session.add()
        db.session.commit()

    cur_speech = current_user.current_speech
    prev_speech = current_user.previous_speech
    return render_template("speech.html", cur=cur_speech, prev=prev_speech)


@main.route("/handbook", methods=["GET", "POST"])
@login_required
def handbook():
    handbooks = Handbook.query.all()
    if request.method == "POST":
        condition = request.form.get("condition")
        if condition == "upload":
            pass
        else:
            action = request.form.get("action")
            book_id = request.form.get("id")
            book = Handbook.query.filter_by(public_id=book_id)
            if action == "delete":
                if book.active:
                    book.active = False
                    db.session.add()
                    db.session.commit()
            else:
                if not book.active:
                    book.active = True
                    db.session.add()
                    db.session.commit()
        return render_template("handbook.html", handbooks=handbooks)
    return render_template("handbook.html", handbooks=handbooks)


@main.route("/view_logs")
@login_required
def view_logs():
    logs = Userlogs.query.all()
    return render_template("logs.html", logs=logs)

