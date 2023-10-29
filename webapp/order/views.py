from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from webapp.db import db
from datetime import datetime

from webapp.order.models import Order, Order_line, Line_status, Status
from webapp.user.models import User
from webapp.product.models import Product

blueprint = Blueprint('order', __name__, url_prefix='/order')

@blueprint.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html',orders=orders)


@blueprint.route('/order/<product_id>')
def order_view(product_id):
    # Проверяем, есть ли заказ у текущего пользователя?
    current_order = Order.query.join(User).filter(User.id == current_user.id).first()
    # Если заказ есть, то пока просто отображаем страницу заказа
    if current_order:
        flash('У вас есть созданный заказ')
        return render_template('order.html', order=current_order)
    # Если заказа нет, то создаем заказ, позицию заказа и статус позиции заказа = "В корзине"
    else:
        product = Product.query.filter(Product.id == product_id).first_or_404()
        product_cost = 0
        if product:
            for components in product.product_component:
                for line in components.components.price:
                    product_cost += line.cost * (1 - line.discount)
            product_cost += product.product_labor.cost
        order = Order(user_id=current_user.id)
        db.session.add(order)
        db.session.commit()
        # После выполнения db.session.commit() в модели появляется id записи, его сразу же можго использовать: print(order.id)

        product = Order_line(order_id=order.id, product_id=product_id, quantity=1, total_cost=product_cost)
        db.session.add(product)
        db.session.commit()

        line_status = Line_status(line_id=order.id, datetime=datetime.now(), status_id=1)
        db.session.add(line_status)
        db.session.commit()
        
        flash(f'Заказ {order.id} создан')
        # После создания заказа переходим на страницу заказа.
        # Так как есть двойной вызов current_order, нужно подумать как лучше сделать.
        current_order = Order.query.join(User).filter(User.id == current_user.id).first()
        return render_template('order.html', order=current_order)
    
