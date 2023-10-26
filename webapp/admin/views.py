from flask_login import login_required, current_user
from flask import Blueprint
from flask_admin import Admin

from webapp.db import db
from webapp.admin import AdminView, MyAdminIndexView
from webapp.user.models import User
from webapp.product.models import Product, Component, Image, Price, Labor, Product_Component, Product_Image, Component_Image

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@login_required
def admin_index():
    if current_user.is_admin:
        return 'Привет админ'
    else:
        return 'Ты не админ!'

admin = Admin(blueprint, index_view=MyAdminIndexView())
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Product, db.session))
admin.add_view(AdminView(Component, db.session))
admin.add_view(AdminView(Image, db.session))
admin.add_view(AdminView(Price, db.session))
admin.add_view(AdminView(Labor, db.session))
admin.add_view(AdminView(Product_Component, db.session))
admin.add_view(AdminView(Product_Image, db.session))
admin.add_view(AdminView(Component_Image, db.session))