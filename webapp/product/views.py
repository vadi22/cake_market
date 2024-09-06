from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from webapp.product.forms import CommentForm
from webapp.product.models import Product, Component, Image, Price, Labor, Product_Component, Comment
from webapp import db
from webapp.utils import get_redirect_target

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
    components_list = []
    product_cost = 0
    form = CommentForm(product_id=product_id)
    if product:
        # # Вытаскиваем фотографии продукта. Пока их всегда 1, но можно хранит несколько.
        # for image in product.product_images:
        #     images_list.append(image.images)     
        # Считаем стоимость торта, получая все компоненты, их стоимость и скидку на них
        for components in product.product_component:
            for line in components.components.price:
                # подсчитываем стоимость компонентов
                product_cost += line.cost * (1 - line.discount)
            # Собираем список компонентов
            components_list.append(components.components.name)
        # Прибавляем стоимость работы
        product_cost += product.product_labor.cost
        production_time = product.product_labor.hours
    return render_template(
        'product.html', 
            product = product, 
            # images = images_list,
            product_cost = int(product_cost),
            production_time = int(production_time),
            components_list = components_list,
            form = form,
    )

@blueprint.route('/comment/', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        if Product.query.filter(Product.id == form.product_id.data).first():
            comment = Comment(text=form.comment_text.data, product_id=form.product_id.data, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            flash('Комментарий успешно добавлен')
            return redirect(url_for('product.product_view', product_id= form.product_id.data))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в заполнении поля "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(get_redirect_target())