from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user
from webapp.db import db
from datetime import datetime

from webapp.order.models import Order, Order_line, Line_status, Status
from webapp.user.models import User
from webapp.product.models import Product

blueprint = Blueprint("order", __name__, url_prefix="/order")


def summ_product_cost(product_id):
    product = Product.query.filter(Product.id == product_id).first_or_404()
    product_cost = 0
    if product:
        for components in product.product_component:
            for line in components.components.price:
                product_cost += line.cost * (1 - line.discount)
        product_cost += product.product_labor.cost
    return product_cost


def order_create(product_id):
    order = Order(user_id=current_user.id)
    db.session.add(order)
    db.session.commit()
    # Считаем стоимость продукта
    product_cost = summ_product_cost(product_id)
    # После выполнения db.session.commit() в модели появляется id записи, его сразу же можго использовать: print(order.id)
    product = Order_line(
        order_id=order.id, product_id=product_id, quantity=1, total_cost=product_cost
    )
    db.session.add(product)
    db.session.commit()
    # Устанавливаем статус на позицию, статус "В корзине"
    # Решил что пусть будет лишний раз обновляться статус
    line_status = Line_status(line_id=order.id, datetime=datetime.now(), status_id=1)
    db.session.add(line_status)
    db.session.commit()

    flash(f"Заказ {order.id} создан")
    # После создания заказа переходим на страницу заказа.
    # Так как есть двойной вызов current_order, нужно подумать как лучше сделать.
    current_order = Order.query.join(User).filter(User.id == current_user.id).first()
    return render_template("order.html", order=current_order)


@blueprint.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        try:
            if current_user.is_admin:
                orders = Order.query.all()
                statuses = Status.query.all()
                return render_template("orders.html", orders=orders, statuses=statuses)
            else:
                flash("Вы не авторизованы для данной операции")
                return redirect(url_for("product.catalog"))
        except AttributeError:
            flash("Вы не авторизованы для данной операции")
            return redirect(url_for("product.catalog"))
    if request.method == "POST":
        try:
            if current_user.is_admin:
                # Ищем все значения статусов и там где он выставлен новым (он числовой),
                # мы его меняем в базе данных
                for key in request.form:
                    if key.startswith("new_status."):
                        id_ = key.partition(".")[-1]
                        try:
                            value = int(request.form[key])
                            print(f"Для строки {id_} новый статус {value}")
                            line_status = Line_status(
                                line_id=id_, status_id=value, datetime=datetime.now()
                            )
                            db.session.add(line_status)
                            db.session.commit()
                        except:
                            pass
                # orders = Order.query.all()
                # statuses = Status.query.all()
                # return render_template('orders.html',orders=orders, statuses=statuses)
                return redirect(url_for("order.orders"))
        except AttributeError:
            flash("Вы не авторизованы для данной операции")
            return redirect(url_for("product.catalog"))


@blueprint.route("/order", methods=["GET", "POST"])
def order_view():
    if request.method == "GET":
        # Проверяем, есть ли заказ у текущего пользователя?
        try:
            current_order = (
                Order.query.join(User)
                .join(Order_line)
                .join(Line_status)
                .filter(User.id == current_user.id, Line_status.status_id == 1)
                .first()
            )
            # Если заказ есть, то пока просто отображаем страницу заказа
            if current_order:
                return render_template("order.html", order=current_order)
            # Если заказа нет, то просим добавить товар в корзину
            else:
                flash("Ваша корзина пуста, сначала добавьте товар в корзину")
                return redirect(url_for("product.catalog"))
        except AttributeError:
            flash(
                "Вы не авторизованы. Корзина доступна только авторизованным пользователям."
            )
            return redirect(url_for("product.catalog"))
    if request.method == "POST":
        try:
            # Изменение количества в корзине
            for key in request.form:
                if key.startswith("new_quantity."):
                    id_ = key.split(".")[-1]
                    old_quantity = int(key.split(".")[-2])
                    try:
                        value = int(request.form[key])
                        # Если новое кол-во равно нулю, то количество в заказе снижаем до нуля, ставим статус 4 (удалено)
                        if value == 0:
                            flash(f"Позиция удалена")
                            order_line = db.session.query(Order_line).get(id_)
                            order_line.quantity = value
                            db.session.commit()
                            line_status = Line_status(
                                line_id=id_, datetime=datetime.now(), status_id=4
                            )
                            db.session.add(line_status)
                            db.session.commit()
                        # Если новое кол-во просто отличается от старого, то меняем количество, статус не меняем.
                        elif old_quantity != value:
                            flash(f"Заказ пересчитан")
                            order_line = db.session.query(Order_line).get(id_)
                            order_line.quantity = value
                            db.session.commit()
                    except:
                        pass
            return redirect(url_for("order.order_view"))
        except AttributeError:
            flash("Вы не авторизованы для данной операции")
            return redirect(url_for("product.catalog"))


@blueprint.route("/<product_id>")
def order_change(product_id):
    try:
        # Если заказ есть, то пока просто отображаем страницу заказа
        current_order = (
            Order.query.join(User)
            .join(Order_line)
            .join(Line_status)
            .filter(User.id == current_user.id, Line_status.status_id == 1)
            .first()
        )
        if current_order:
            # Ищу, есть ли заказ в корзине
            # Если есть, то смотрим, есть ли в корзине выбранный товар
            product_in_order = Order_line.query.filter(
                Order_line.order_id == current_order.id,
                Order_line.product_id == product_id,
            ).first()
            # Если такой товар есть, то добавляю +1 к количеству
            if product_in_order:
                product_in_order.quantity += 1
                db.session.commit()
            # Если нет, то добавляем к заказу позицию с этим товаром
            else:
                product_cost = summ_product_cost(product_id)
                product_in_order = Order_line(
                    order_id=product_in_order.id,
                    product_id=product_id,
                    quantity=1,
                    total_cost=product_cost,
                )
                db.session.add(product_in_order)
                db.session.commit()
            # Устанавливаем статус на позицию, статус "В корзине"
            # Решил что пусть будет лишний раз обновляться статус
            line_status = Line_status(
                line_id=product_in_order.id,
                datetime=datetime.now(),
                status_id=1,
            )
            db.session.add(line_status)
            db.session.commit()
            flash(f"Товар добавлен в корзину")
            # После создания заказа переходим на страницу заказа.
            return redirect(url_for("order.order_view"))
        # Если заказа нет, то создаем заказ, позицию заказа и статус позиции заказа = "В корзине"
        else:
            order_create(product_id)
    except AttributeError:
        flash(
            "Вы не авторизованы. Добавить материал в корзину можно только после авторизации."
        )
        return redirect(url_for("product.catalog"))
