from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль',validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить',render_kw={"class": "btn btn-primary"})