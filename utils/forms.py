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

class VareForm(FlaskForm):
    """Skjema for å legge til ny vare på handlelisten"""
    vare = StringField("Ny vare", validators=[InputRequired()])
    submit = SubmitField("Legg til")

