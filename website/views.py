from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,Suggestions
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user) 

@views.route('/pterodactyl')
@login_required
def pterodactyl():
    return render_template('pterodactyl.html', user=current_user)

@views.route('/guacamole')
@login_required
def Guacamole():
    return render_template('guacamole.html', user=current_user)

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
            print(Mdays)
        else:
            flash('Must be a number.', category='error')
    return render_template('minecraftdays.html', user=current_user)

@views.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    if request.method == 'POST':
        data = request.form
        print(data)
        email = request.form.get('email')
        suggestion = request.form.get('suggestion')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('you can only send one suggestion per email.', category='error')
        elif len(email) < 3:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(suggestion) < 4:
            flash('suggestion must be at least 4 characters.', category='error')
        else:
            new_user = User(email=email)
            db.session.add(new_user)
            new_suggestion  = Suggestions(data=suggestion)
            db.session.add(new_suggestion)
            db.session.commit()
            flash('Thanks!', category='success')
            return redirect(url_for('views.suggestions'))         
    return render_template('suggestions.html', user=current_user)    