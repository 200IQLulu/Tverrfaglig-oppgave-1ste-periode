from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    name = StringField("Navn", validators=[InputRequired()])
    username = StringField("Brukernavn", validators=[InputRequired()])
    password = PasswordField("Passord", validators=[InputRequired()])
    submit = SubmitField("Registrer")

class LoginForm(FlaskForm):
    username = StringField("Brukernavn", validators=[InputRequired()])
    password = PasswordField("Passord", validators=[InputRequired()])
    submit = SubmitField("Logg inn")

