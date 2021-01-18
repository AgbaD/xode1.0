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
from ..models import Admin, User
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
    pass

