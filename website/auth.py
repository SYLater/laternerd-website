import os
import os.path
import shutil
from os import path

from flask import (Blueprint, Response, current_app, flash, redirect,
                   render_template, request, send_from_directory, session,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user
from requests import Response
from sqlalchemy import update
from werkzeug.datastructures import FileStorage
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from PIL import Image

from . import db
from .models import Suggestions, User

auth = Blueprint('auth', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        Email = request.form.get('Email')
        password = request.form.get('password')
        UserName = request.form.get('Username')
        icon = 'static/images/usericons/default_icon.png'

        user = User.query.filter_by(Email=Email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(Email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(Email=Email, password=generate_password_hash(
                password, method='sha256'), UserName=UserName, icon=icon)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Email = request.form.get('Email')
        password = request.form.get('password')
        user = User.query.filter_by(Email=Email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/account', methods=['GET', 'POST'])
@login_required
def Account():
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':

        icon = request.files['icon']
        iconName = secure_filename(icon.filename)
        RawIconName = (current_app.config['UPLOAD_FOLDER'] + "/" + iconName)
        icon_extention = os.path.splitext(RawIconName)[1]
        FullIconDir = current_app.config['UPLOAD_FOLDER'] + "/" + user.UserName + icon_extention
        FormattedIconName = user.UserName + icon_extention
        

        if 'icon' not in request.files:
            flash('No file part')
            return redirect(request.url)

        if icon.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if path.exists(FullIconDir):
            os.remove(FullIconDir)


        if icon and allowed_file(icon.filename):
            icon.save(os.path.join(current_app.config['UPLOAD_FOLDER'], iconName))
            os.rename(RawIconName, FullIconDir)
            
            for FormattedIconName in os.listdir(current_app.config['UPLOAD_FOLDER']):
                with Image.open (str(FullIconDir)) as im:
                    x= im.size
                    y = im.size
                    x, y = im.size
                totalsize = x*y
                print(x)
                print(y)

            if x > 1000:
                flash('Icon needs to be less than 1000x1000')
                os.remove(FullIconDir)
                return redirect(request.url)     
            if y > 1000:
                flash('Icon needs to be less than 1000x1000')
                os.remove(FullIconDir)
                return redirect(request.url)                    

            file_length = os.stat(FullIconDir).st_size
            if file_length > 3000000:
                flash('Icon needs to be less than 3MB')
                os.remove(FullIconDir)
                return redirect(request.url)
            
            IconDirSite = ('static/images/usericons/' + user.UserName + icon_extention)
            user.icon = IconDirSite
            db.session.commit()
            flash('Image successfully uploaded and displayed below')
            return render_template('account.html', filename=iconName, user=current_user)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template('account.html', user=current_user)
