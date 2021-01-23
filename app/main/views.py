#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

# packages
from flask import *
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

# user created
from . import main
from .. import db
from ..models import Admin, Userlogs, Handbook
from ..schema import validate_login

# inbuilt
from datetime import datetime
import uuid
import os

ALLOWED_EXTENSIONS = {'pdf', 'md', 'txt'}


@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")

        data = {"email": email, "password": password}
        # check schema
        schema_val = validate_login(data)
        if schema_val["msg"] != "success":
            flash(schema_val["error"])
            return render_template('login.html', data=data)

        admin = Admin.query.filter_by(email=email).first()
        if not admin:
            flash("Account not found please check email.")
            return render_template("login.html", data=data)
        if not check_password_hash(admin.password_hash, password):
            flash("Password incorrect!")
            return render_template("login.html", data=data)

        login_user(admin)
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
            current_user.facebook = "http://" + request.form.get("facebook")
        if request.form.get("twitter"):
            current_user.twitter = "http://" + request.form.get("twitter")
        if request.form.get("instagram"):
            current_user.instagram = "http://" + request.form.get("instagram")

        db.session.add(current_user)
        db.session.commit()
    
    social = {}

    try:
        fb = current_user.facebook
        social["fb"] = fb
    except:
        social["fb"] = "#"

    try:
        tw = current_user.twitter
        social["tw"] = tw 
    except:
        social["tw"] = "#"

    try:
        ig = current_user.instagram
        social["ig"] = ig
    except:
        social["ig"] = "#"
    return render_template("socials.html", data=social)


@main.route("/speech", methods=["GET", "POST"])
@login_required
def speech():
    if request.method == "POST":
        speech_now = request.form.get("speech")
        cur = current_user.current_speech
        if cur:
            current_user.previous_speech = cur
        current_user.current_speech = speech_now

        db.session.add(current_user)
        db.session.commit()

    try:
        cur_speech = current_user.current_speech
    except:
        cur_speech = None

    try:
        prev_speech = current_user.previous_speech
    except:
        prev_speech = None
    return render_template("speech.html", cur=cur_speech, prev=prev_speech)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/handbook/<int:page_num>", methods=["GET", "POST"])
@login_required
def handbook(page_num):
    if request.method == "POST":
        try:
            condition = request.form.get("condition")
        except:
            condition = None
        if condition == "upload":
            file = request.files["file"]
            name = request.form.get("rename")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                public_id = str(uuid.uuid4())
                book = Handbook(public_id=public_id, book_name=filename, book_path=file_path, uploaded_on=datetime.utcnow())
                db.session.add(book)
                db.session.commit()
            else:
                print("invalid file")
        else:
            action = request.form.get("action")
            book_id = request.form.get("id")
            book = Handbook.query.filter_by(public_id=book_id).first()
            if not book: # should never happen
                return redirect(url_for('main.internal_server_error'))
            if action == "delete":
                print(book.public_id)
                if book.active:
                    book.active = False
                    db.session.add(book)
                    db.session.commit()
            else:
                if not book.active:
                    book.active = True
                    db.session.add(book)
                    db.session.commit()
        handbooks = Handbook.query.paginate(per_page=5, page=page_num, error_out=True)
        return render_template("handbook.html", handbooks=handbooks)
    handbooks = Handbook.query.paginate(per_page=5, page=page_num, error_out=True)
    if handbooks:
        return render_template("handbook.html", handbooks=handbooks)
    else:
        return render_template("handbook.html", handbooks=None)


@main.route('/handbooks/<filename>')
def view_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)


@main.route("/view_logs/<int:page_num>")
@login_required
def view_logs(page_num):
    logs = Userlogs.query.paginate(per_page=5, page=page_num, error_out=True)
    if logs:
        return render_template("logs.html", logs=logs)
    else:
        return render_template("logs.html", logs=None)



# still gatta work csrf for frontend