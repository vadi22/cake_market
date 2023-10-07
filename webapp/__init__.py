from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from webapp.admin import AdminView, MyAdminIndexView
from webapp.models import db, User, Product, Component, Image, Price, Labor, Product_Component, Product_Image, Component_Image
from webapp.forms import LoginForm, RegistrationForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
    

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
        
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
    
    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))
    
    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))
    
    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ'
        else:
            return 'Ты не админ!'
        
    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        title = "Регистрация"
        return render_template('registration.html', page_title=title, form=form)
    
    @app.route('/process-reg', methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!')
            return redirect(url_for('login'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
            return redirect(url_for('register'))
        
    @app.route('/user/<email>')
    @login_required
    def user(email):
        user = User.query.filter_by(email = email).first()
        if user == None:
            flash('User ' + email + ' not found.')
            return redirect(url_for('index'))
        return 'привет'
        # return render_template('user.html',
        #     user = user,
        #     posts = posts)
        

    admin = Admin(app, index_view=MyAdminIndexView())
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Product, db.session))
    admin.add_view(AdminView(Component, db.session))
    admin.add_view(AdminView(Image, db.session))
    admin.add_view(AdminView(Price, db.session))
    admin.add_view(AdminView(Labor, db.session))
    admin.add_view(AdminView(Product_Component, db.session))
    admin.add_view(AdminView(Product_Image, db.session))
    admin.add_view(AdminView(Component_Image, db.session))




    return app




