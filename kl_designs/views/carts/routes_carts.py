from datetime import datetime

from flask import (render_template, url_for, flash, redirect, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy import func
from kl_designs.models import Item, Product, Category
from kl_designs import db
from kl_designs.views.products.forms import Product_Item_Form
from kl_designs.views.utils import send_order_email

carts = Blueprint('carts', __name__)


@carts.route("/cart/int:<productid>/new", methods=['GET', 'POST'])
@login_required
def product_cart(productid):
    form = Product_Item_Form()
    product = Product.query.get_or_404(productid)


    if form.validate_on_submit():
        add_item = Item(
                        quantity=form.quantity.data,
                        size=form.ring_size.data,

                        product_name= product.product_name,
                        category_name=product.category_id,
                        description= product.description,
                        image_file= product.image_file,
                        image_file_2=product.image_file_2,
                        image_file_3=product.image_file_3,
                        price= product.price,

                        author=current_user)

        db.session.add(add_item)
        db.session.commit()

        flash('Tu producto fue agregado exitosament al carrito!', 'success')
        return redirect(url_for('products.all_product'))

    return render_template('product/product_details_plus_cart_add.html',
                           product=product, form=form,
                           )


@carts.route("/cart/int:<productid>/add", methods=['GET', 'POST'])
@login_required
def add_one_product_to_cart(productid):
    product = Product.query.get_or_404(productid)
    add_item = Item(quantity=1,
                    product_name= product.product_name,
                    description= product.description,

                    image_file= product.image_file,
                    image_file_2=product.image_file_2,
                    image_file_3=product.image_file_3,

                    price= product.price,
                    author=current_user)

    db.session.add(add_item)
    db.session.commit()

    flash('Tu producto fue agregado exitosament al carrito!', 'success')
    return redirect(url_for('products.all_product'))

    return render_template('product/product_details_plus_cart_add.html', product=product, form=form)


@carts.route("/delete_cart_item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_cart_item(item_id):
    cart_item_delete = Item.query.get_or_404(item_id)

    db.session.delete(cart_item_delete)
    db.session.commit()
    flash('El producto fue eliminado!', 'danger')
    return redirect(url_for('carts.user_carts'))


@carts.route("/user_carts")
def user_carts():
    items = Item.query.filter_by(author=current_user).filter_by(status='pending')
    total = db.session.query(func.sum(Item.price)).filter_by(author=current_user).filter_by(status='pending').scalar()
    Order_total = db.session.query(func.sum(Item.price * Item.quantity)).filter_by(author=current_user).filter_by(status='pending').scalar()

    Ordered_total = Item.query.filter_by(author=current_user).filter_by(status='Ordered')

    return render_template('cart/user_cart.html',
                           items=items, total=total,
                           Order_total=Order_total, Ordered_total=Ordered_total)


@carts.route("/cart/int:<itemid>", methods=['GET', 'POST'])
def cart_item(itemid):
    cart_item = Item.query.get_or_404(itemid)
    return render_template('cart/item_cart_detail.html', cart_item=cart_item)


@carts.route("/order_items_in_cart", methods=['GET', 'POST'])
def order_items():
    order_items = Item.query.filter_by(author=current_user).filter_by(status='pending')\
        .update({ Item.status: 'Ordered', Item.order_date: datetime.utcnow()})

    db.session.commit()


    flash('Tu Orden fue encargada!', 'success')
    return redirect(url_for('orders.user_order'))


