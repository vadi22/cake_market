from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired
from webapp.models import User


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
   
    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')
        

class AddressForm(FlaskForm):
    city = StringField('Город', validators=[InputRequired()],  render_kw={"class": "form-control"})
    district = StringField('Район', validators=[InputRequired()],  render_kw={"class": "form-control"})
    street = StringField('Улица', validators=[InputRequired()],  render_kw={"class": "form-control"})
    home = StringField('Дом', validators=[InputRequired()],  render_kw={"class": "form-control"})
    apartment = StringField('Квартира', validators=[InputRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Сохранить', validators=[InputRequired()], render_kw={"class": "btn btn-primary"})


