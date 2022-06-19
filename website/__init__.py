import os
import urllib.request
import time
from distutils.log import debug
from operator import imod
from os import path
from flask_socketio import SocketIO, send
from flask import (Blueprint, Flask, Response, flash, redirect,
                   render_template, request, send_from_directory, session, url_for)
from flask_login import LoginManager, current_user, login_manager
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

socketio = SocketIO()



db = SQLAlchemy()
DB_NAME = 'database.db'
UPLOAD_FOLDER = 'website/static/images/usericons'



def create_app():
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'IloveLilly'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://later:flower7@192.168.0.87:33060/nerd'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///' + DB_NAME
    db.init_app(app)
    db.update(User)
    from .auth import auth
    from .models import History, Suggestions, User
    from .routes import routes
    # from .simon import simon
    from .views import views

    app.register_blueprint(routes)
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(simon, url_prefix='/')

    db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404


    @socketio.on('joined', namespace='/chat')
    def joined(message):
        """Sent by clients when they enter a room.
        A status message is broadcast to all people in the room."""
        room = session.get('room')
        join_room(room)
        emit('status', {'msg': session.get('name') +
             ' has entered the room.'}, room=room, user=current_user)

    @socketio.on('text', namespace='/chat')
    def text(message):
        """Sent by a client when the user entered a new message.
        The message is sent to all people in the room."""
        room = session.get('room')
        ChatHistory = History(msgh=session.get('name') + ':' + message['msg'])
        db.session.add(ChatHistory)
        db.session.commit() 
        print(session.get('name') + ':' + message['msg'])
        emit('message', {'msg': session.get('name') + ' 1:17 \n ' + message['msg']}, room=room, user=current_user)

    @socketio.on('left', namespace='/chat')
    def left(message):
        """Sent by clients when they leave a room.
        A status message is broadcast to all people in the room."""
        room = session.get('room')
        leave_room(room)
        emit('status', {'msg': session.get('name') +
             ' has left the room.'}, room=room, user=current_user)

        


    socketio.init_app(app, cors_allowed_origins="*")
    return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
