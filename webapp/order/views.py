from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from webapp.order.models import Order, Order_line, Line_status, Status

blueprint = Blueprint('order', __name__, url_prefix='/order')

@blueprint.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html',orders=orders)


@blueprint.route('/<int:order_id>')
def order_view(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    if order:
        flash('Это пока просто загрушка для заказа')
        return render_template('order.html')
    else:
        flash('Такого заказа не существует')
        return redirect(url_for('order.orders'))
