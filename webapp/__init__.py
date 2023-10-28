from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.db import db
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint
from webapp.product.views import blueprint as product_blueprint
from webapp.order.views import blueprint as order_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    app.register_blueprint(product_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(order_blueprint)
    

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
        
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
