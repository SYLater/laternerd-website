import os
from flask import (Blueprint, flash, redirect, render_template, request, send_file,
                   send_from_directory, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from . import db
from .forms import LoginForm
from .models import History

routes = Blueprint('routes', __name__)

@routes.route('/user', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form:
        session['name'] = current_user.UserName
        session['room'] = 'room'
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form, user=current_user)

@routes.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    history = History.query.all()
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, user=current_user, history=history)
