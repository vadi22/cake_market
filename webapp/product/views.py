from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from webapp.product.models import Product, Component, Image, Price, Labor, Product_Component, Product_Image, Component_Image

blueprint = Blueprint('product', __name__, url_prefix='/product')

@blueprint.route('/catalog')
def catalog():
    products = Product.query.all()
    return render_template(
        'catalog.html', 
            products=products, 
    )
    pass

@blueprint.route('/<int:product_id>')
def product_view(product_id):
    product = Product.query.filter(Product.id == product_id).first_or_404()
    images_list = []
    product_cost = 0
    if product:
        # Вытаскиваем фотографии продукта. Пока их всегда 1, но можно хранит несколько.
        for image in product.product_images:
            images_list.append(image.images)     
        # Считаем стоимость торта, получая все компоненты, их стоимость и скидку на них
        for costs in product.product_component:
            for line in costs.components.price:
                # подсчитываем стоимость компонентов
                product_cost += line.cost * (1 - line.discount)
        # Прибавляем стоимость работы
        product_cost += product.product_labor.cost
        production_time = product.product_labor.hours
    return render_template(
        'product.html', 
            product=product, 
            images = images_list,
            product_cost = int(product_cost),
            production_time = int(production_time)
    )