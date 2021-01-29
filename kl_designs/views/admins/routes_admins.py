from datetime import datetime

from flask import render_template, url_for, flash, redirect, Blueprint, request
from flask_login import login_required
from sqlalchemy import func

from kl_designs import db
from kl_designs.models import User, Category, Product, Item, Design, Taller, AnillosCompromiso
from kl_designs.views.admins.forms import Delivery_Form, Admin_Update_User_AccountForm
from kl_designs.views.utils import save_picture

admins = Blueprint('admins', __name__)


@admins.route("/admin", methods=['GET', 'POST'])
@login_required
def index():
    users = User.query.all()
    user_count = db.session.query(User.id).count()

    categories = Category.query.all()
    category_count = db.session.query(Category.id).count()

    products = Product.query.all()
    product_count = db.session.query(Product.productid).count()

    designs = Design.query.all()
    design_count = db.session.query(Design.id).count()

    tallers = Taller.query.all()
    taller_count = db.session.query(Taller.id).count()

    anillos = AnillosCompromiso.query.all()
    anillo_count = db.session.query(AnillosCompromiso.id).count()

    items_ordered = Item.query.filter_by(status='Ordered')
    items_payed = Item.query.filter_by(status='Payed')

    total_pending = db.session.query(func.sum(Item.price)).filter_by(status='pending').scalar()
    total_ordered = db.session.query(func.sum(Item.price)).filter_by(status='Ordered').scalar()

    return render_template('admin/admin.html',
                           user_count=user_count, users=users,
                           categories=categories, category_count=category_count,
                           products=products, product_count=product_count,
                           designs=designs, design_count=design_count,
                           items_payed=items_payed, items_ordered=items_ordered,
                           total_pending=total_pending, total_ordered=total_ordered,
                           tallers=tallers, taller_count=taller_count,
                           anillos=anillos, anillo_count=anillo_count,
                           )


@admins.route("/move_to_payed/<itemid>", methods=['GET', 'POST'])
@login_required
def move_to_pay_items(itemid):
    cart_item = Item.query.filter_by(itemid=int(itemid)).first()
    cart_item.status = "Payed"

    db.session.commit()
    ##
    flash('El Producto fue Pagado!... Ahora solo neceistamos enviarlo', 'success')
    return redirect(url_for('admins.index'))


######################## Delivery and Reception ##############################################

@admins.route("/admin/delivery/int:<itemid>", methods=['GET', 'POST'])
@login_required
def add_delivery(itemid):
    form = Delivery_Form()
    item = Item.query.filter_by(itemid=int(itemid)).first()

    if form.validate_on_submit():
        item.delivery_date = datetime.utcnow()
        item.deliveryid = form.deliveryid.data
        item.carrier = form.carrier.data
        item.status = "Sent"

        db.session.commit()
        flash('El Producto fue Enviado!', 'success')
        return redirect(url_for('admins.index'))
    return render_template('admin/new_delivery.html', item=item, form=form)


@admins.route("/admin/received/int:<itemid>", methods=['GET', 'POST'])
@login_required
def delivery_received(itemid):

    delivery_item = Item.query.filter_by(itemid=int(itemid)).first()
    delivery_item.status = "Received"
    delivery_item.received_date = datetime.utcnow()

    db.session.commit()

    #send_sent_email(order_items, author=current_user)

    flash('La Orden fue Recivida!', 'success')
    return redirect(url_for('admins.delivery_stats'))


############################# Views #############################################

@admins.route("/admin/delivery_stats", methods=['GET', 'POST'])
@login_required
def delivery_stats():
    delivery_status = Item.query.filter(Item.status != 'pending')

    delivery_pending = Item.query.filter(Item.status == 'Payed').count()
    delivery_sent = Item.query.filter(Item.status == 'Sent').count()
    delivery_received = Item.query.filter(Item.status == 'Received').count()


    return render_template('admin/delivery.html',
                           delivery_status=delivery_status, delivery_pending=delivery_pending,
                           delivery_sent=delivery_sent, delivery_received=delivery_received,
                           )


@admins.route("/admin/delivery_detail/<itemid>", methods=['GET', 'POST'])
@login_required
def delivery_detail(itemid):
    cart_item = Item.query.get_or_404(itemid)
    category_count = db.session.query(Category.id).count()

    user_count = db.session.query(User.id).count()
    product_count = db.session.query(Product.productid).count()

    return render_template('admin/delivery_detail.html', cart_item=cart_item)


########################## Items and Users ###############################

@admins.route("/admin/user_details", methods=['GET', 'POST'])
@login_required
def user_stats():
    items_all_status = Item.query.all()

    category_count = db.session.query(Category.id).count()

    user_count = db.session.query(User.id).count()
    product_count = db.session.query(Product.productid).count()

    revenue_pending = db.session.query(func.sum(Item.price * Item.quantity)).filter_by(status='pending').scalar()
    revenue_ordered = db.session.query(func.sum(Item.price * Item.quantity)).filter_by(status='Ordered').scalar()
    payed_ordered = db.session.query(func.sum(Item.price * Item.quantity)).filter_by(status='Payed').scalar()

    return render_template('admin/admin_user_stats.html', items_all_status=items_all_status,
                           revenue_pending=revenue_pending, revenue_ordered=revenue_ordered,
                           payed_ordered=payed_ordered, user_count=user_count,
                           category_count=category_count, product_count=product_count
                           )


@admins.route("/delete_item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_item(item_id):
    item_delete = Item.query.get_or_404(item_id)

    db.session.delete(item_delete)
    db.session.commit()
    flash('Su Producto fue borrado!', 'danger')
    return redirect(url_for('admins.user_stats'))


@admins.route("/user_account/<int:id>")
def user_account(id):
    user_detail = User.query.filter_by(id=id).first_or_404()
    items_all_status = Item.query.filter_by(author=user_detail)

    revenue_pending = db.session.query(func.sum(Item.price * Item.quantity)).filter_by(status='pending').filter_by(author=user_detail).scalar()
    revenue_ordered = db.session.query(func.sum(Item.price * Item.quantity)).filter_by(status='Ordered').filter_by(author=user_detail).scalar()
    payed_ordered = db.session.query(func.sum(Item.price * Item.quantity)).filter_by(status='Payed').filter_by(author=user_detail).scalar()

    form = Admin_Update_User_AccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user_detail.image_file = picture_file

        user_detail.fname = form.fname.data
        user_detail.email = form.email.data

        user_detail.complete_address1 = form.complete_address1.data
        user_detail.zipcode = form.zipcode.data
        user_detail.phone = form.phone.data


        db.session.commit()
        flash('Tu Cuenta ha sido actualizada!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.fname.data = user_detail.fname
        form.email.data = user_detail.email
        form.complete_address1.data = user_detail.complete_address1
        form.zipcode.data = user_detail.zipcode
        form.phone.data = user_detail.phone


    image_file = url_for('static', filename='photos/' + user_detail.image_file)


    return render_template('admin/user_detail.html',
                           user_detail=user_detail, items_all_status=items_all_status,
                           image_file=image_file, form=form,
                           revenue_pending=revenue_pending, revenue_ordered=revenue_ordered,
                           payed_ordered=payed_ordered)

@admins.route("/admin/user_roles", methods=['GET', 'POST'])
@login_required
def user_roles():
    user_count = db.session.query(User.id).count()
    user = User.query.all()
    return render_template('admin/user_role.html',
                           user_count=user_count, user=user)


@admins.route("/admin/update_user_role/<int:id>", methods=['GET', 'POST'])
@login_required
def update_user_role(id):
    user_detail = User.query.filter_by(id=id).first_or_404()

    form = Admin_Update_User_AccountForm()
    if form.validate_on_submit():
        user_detail.fname = form.fname.data
        user_detail.email = form.email.data
        user_detail.role = form.role.data

        db.session.commit()
        flash('User Data was Updated!', 'success')
        return redirect(url_for('admins.index'))
    elif request.method == 'GET':
        form.fname.data = user_detail.fname
        form.email.data = user_detail.email
        form.role.data = user_detail.role


    return render_template('admin/update_user_detail.html',
                           user_detail=user_detail, form=form,
                           )


