import os
import os.path
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

from . import db
from .models import History, Suggestions, User

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        colour = request.form.get('colorchangerbtn')
        print(colour)
    return render_template('home.html', user=current_user) 

@views.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(views.root_path, 'static/images'),'favicon.ico', mimetype='image/favico.icon')

@views.route('/pterodactyl')
@login_required
def pterodactyl():
    return render_template('pterodactyl.html', user=current_user)

@views.route('/guacamole')
@login_required
def Guacamole():
    return render_template('guacamole.html', user=current_user)

@views.route('/alldata')
@login_required
def alldata():
    suggestions = Suggestions.query.all()
    users = User.query.all()
    history = History.query.all()
    return render_template('alldata.html', user=current_user, suggestions=suggestions, users=users, history=history)

@views.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        Mdays = request.form.get('days')

        if Mdays.isdigit():
            minutes = int(Mdays)*20
            hours = int(minutes)/60.000
            days = int(hours)/24
            weeks = int(days)/7
            return render_template("minecraftdays.html", days="%.2f" % days, minutes="%.2f" % minutes, hours="%.2f" % hours, weeks="%.2f" % weeks, user=current_user)
        else:
            flash('Must be a number.', category='error')
    return render_template('minecraftdays.html', user=current_user)

@views.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    if request.method == 'POST':
        email = request.form.get('email')
        suggestion = request.form.get('suggestion')
        if len(email) < 3:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(suggestion) < 4:
            flash('suggestion must be at least 4 characters.', category='error')
        else:
            new_suggestion  = Suggestions(suggestion=suggestion, email=email)
            db.session.add(new_suggestion)
            db.session.commit() 
            flash('Thanks!', category='success')
            return redirect(url_for('views.suggestions'))         
    return render_template('suggestions.html', user=current_user, suggestions=suggestions)    

