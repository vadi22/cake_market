from flask import Flask, render_template, flash, redirect, url_for, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from webapp.admin import AdminView, MyAdminIndexView
from flask_admin import Admin
from webapp.models import db, User, Product, Component, Image, Price, Labor, Product_Component, Product_Image, Component_Image, User_adress
from webapp.forms import LoginForm, RegistrationForm, AddressForm

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




    @app.route('/user/<int:user_id>')
    @login_required
    def user_profile(user_id):
        user = User.query.filter(User.id == user_id).first_or_404()
        adress = User_adress.query.filter(User_adress.user_id == user_id).first_or_404()
        if current_user != user:
            abort(404)
        return render_template(
            'user_profile.html', 
                user=user, 
                page_title = 'Личный кабинет',
                adress = adress,
        )
    

    @app.route('/user/<int:user_id>/edit_profile', methods=['GET', 'POST'])
    @login_required
    def edit_profile(user_id):
        user = User.query.filter(User.id == user_id).first_or_404()
        if current_user != user:
            abort(404)
        form = AddressForm()
        title = "Регистрация"
        return render_template('edit_profile.html', form=form)
    
    @app.route('/edit_adress', methods=['GET', 'POST'])
    def edit_adress():
        form = AddressForm()
        new_adress = User_adress(city=form.city.data, district=form.district.data, street=form.street.data, home=form.home.data, apartment=form.apartment.data, user_id=current_user.id)
        db.session.add(new_adress)
        db.session.commit()
        flash('Адрес принят')
        return redirect(url_for('user_profile', user_id=current_user.id))
    

        # # if form.validate_on_submit():
        # new_adress = User_adress(city=form.city.data, district=form.district.data, street=form.street.data, home=form.home.data, apartment=form.apartment.data, user_id=current_user.id)
        # db.session.add(new_adress)
        # db.session.commit()
        # flash('Адрес принят')
        # return redirect(url_for('user_profile', user_id=user.id))
        # # else:
        # #     flash('Адрес не принят')
        # #     return redirect(url_for('user_profile', user_id=user.id ))

        

    # @app.route('/user/<email')
    # @login_required
    # def user(email):
    #     user = User.query.filter_by(email = email).first()
    #     if user == None:
    #         flash('User ' + email + ' not found.')
    #         return redirect(url_for('index'))
    #     return render_template('user_profile.html', user = user, page_title = 'Личный кабинет')   
    
    return app




