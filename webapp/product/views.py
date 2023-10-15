from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from webapp.product.models import Product, Component, Image, Price, Labor, Product_Component, Product_Image, Component_Image

blueprint = Blueprint('product', __name__, url_prefix='/product')

@blueprint.route('/view', methods=['POST'])
def product_wiew():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Регистрация"
    return render_template('product.html', page_title=title)    