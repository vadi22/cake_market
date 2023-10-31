from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from webapp.user.forms import LoginForm, RegistrationForm, AddressForm, ChangePassForm, ForgotPassForm, ResetPassForm
from webapp.user.models import User, User_adress
from webapp.db import db
from flask_mail import Message, Mail
from webapp import mail
from webapp.config import MAIL_DEFAULT_SENDER

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('index'))

@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template('registration.html', page_title=title, form=form)

@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
        return redirect(url_for('user.register'))

@blueprint.route('/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.filter(User.id == user_id).first_or_404()
    adress = User_adress.query.filter(User_adress.user_id == user_id).first()
    if current_user != user:
        abort(404)
    return render_template(
        'user_profile.html', 
            user=user, 
            page_title = 'Личный кабинет',
            adress = adress,
    )

@blueprint.route('/<int:user_id>/edit_profile', methods=['GET'])
@login_required
def edit_profile(user_id):
    user = User.query.filter(User.id == user_id).first_or_404()
    if current_user != user:
        abort(404)
    form = AddressForm()
    return render_template('edit_profile.html', form=form, )

@blueprint.route('/edit_adress', methods=['GET', 'POST'])
def edit_adress():
    form = AddressForm()
    adress = User_adress.query.filter(User_adress.user_id == current_user.id).first()
    if adress:
        db.session.delete(adress)
    adress = User_adress(city=form.city.data, district=form.district.data, street=form.street.data, home=form.home.data, apartment=form.apartment.data, user_id=current_user.id)
    db.session.add(adress)
    db.session.commit()
    flash('Адрес принят')
    return redirect(url_for('user.user_profile', user_id=current_user.id))

@blueprint.route(
    '/<int:user_id>/change_password',
    methods=['GET', 'POST'],
    )
@login_required
def change_password(user_id):
    user = User.query.filter(User.id == user_id).first_or_404()
    if current_user != user:
        abort(404)
    form = ChangePassForm()
    if form.validate_on_submit():
        if user.check_password(form.password_old.data):
            print(user.set_password(form.password_new.data))
            user.set_password(form.password_new.data)
            db.session.add(user)
            db.session.commit()
            flash('Ваш пароль успешно обновлен', 'success')
            return redirect(url_for('user.user_profile', user_id=user.id))
        else:
            flash('Неверный пароль')
    return render_template(
        '/change_password.html',
        form=form,
        user=user,
    )


def send_mail(user):
    token = user.get_token()
    msg = Message('Востановление пароля', recipients=[user.email], sender=MAIL_DEFAULT_SENDER)
    msg.body = f''' Востановление пароля
{url_for('user.reset_token', token=token,_external=True)}


    '''
    mail.send(msg)


@blueprint.route(
    '/forgot',
    methods=['GET', 'POST'],
    )
def forgot():
    form = ForgotPassForm()
    if form.validate_on_submit():
        print(1)
        flash('Проверьте свою почту')
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user:
            send_mail(user)

    return render_template('forgot.html', form=form)

@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_token(token)
    if user is None:
        flash('Ошибка')
        return redirect(url_for('forgot'))
    
    form = ResetPassForm()
    print(11)
    if form.validate_on_submit():
        print(1)
        user.set_password(form.password_new.data)
        db.session.add(user)
        db.session.commit()
        flash('Ваш пароль успешно обновлен', 'success')
        return redirect(url_for('login'))
    return render_template('change_password_forgot.html', title = 'Изменение пароля', form=form)



