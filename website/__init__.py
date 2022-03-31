from distutils.log import debug
from this import d
from os import path
from flask import Flask, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, current_user
from flask_socketio import emit, join_room, leave_room, SocketIO




socketio = SocketIO()



db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'IloveLilly'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://later:flower7@192.168.0.87:33060/laternerd'
    db.init_app(app)
    

    from .views import views
    from .auth import auth
    from .models import User, Suggestions, History
    from .routes import routes 
    
 
    app.register_blueprint(routes)
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @socketio.on('joined', namespace='/chat')
    def joined(message):
        """Sent by clients when they enter a room.
        A status message is broadcast to all people in the room."""
        room = session.get('room')
        join_room(room)
        emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room,user=current_user)

    @socketio.on('text', namespace='/chat')
    def text(message):
        """Sent by a client when the user entered a new message.
        The message is sent to all people in the room."""
        room = session.get('room')
        emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room,user=current_user)

    @socketio.on('left', namespace='/chat')
    def left(message):
        """Sent by clients when they leave a room.
        A status message is broadcast to all people in the room."""
        room = session.get('room')
        leave_room(room)
        emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room,user=current_user)
    
    socketio.init_app(app, cors_allowed_origins="*")
    return app
