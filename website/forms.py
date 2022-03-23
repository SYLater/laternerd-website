from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = StringField('Room')
    submit = SubmitField('Enter Chatroom')
