from datetime import datetime

import stripe
from flask import (render_template, url_for, flash, redirect, Blueprint, request, jsonify, abort)
from flask_login import current_user, login_required
from sqlalchemy import func
from kl_designs.models import Item
from kl_designs import db
from kl_designs.views.orders.forms import PaymentForm
from kl_designs.views.utils import send_cancel_email, send_payed_email
import json


orders = Blueprint('orders', __name__)

stripe.api_key = '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'
publishable_key = 'pk_live_c4NUXcZKUwZ7NRm2FBlucMl8009zCrdlAB'


@orders.route("/user_order")
@login_required
def user_order():
    items = Item.query.filter_by(author=current_user).filter_by(status='Ordered')
    total = db.session.query(func.sum(Item.price)).filter_by(author=current_user).filter_by(status='Ordered').scalar()

    Order_total = db.session.query(func.sum(Item.price * (Item.quantity))).filter_by(author=current_user).filter_by(status='Ordered').scalar()
    Order_total = str(Order_total)
    Order_total = ("%.2f"%(float(Order_total)))

    return render_template('order/user_order.html',
                           items=items, total=total,
                           Order_total=Order_total)


@orders.route('/checkout', methods=['GET'])
@login_required
def get_checkout_page():
    items = Item.query.filter_by(author=current_user).filter_by(status='Ordered')
    total = db.session.query(func.sum(Item.price)).filter_by(author=current_user).filter_by(status='Ordered').scalar()

    Order_total = db.session.query(func.sum(Item.price * (Item.quantity))).filter_by(author=current_user).filter_by(
        status='Ordered').scalar()
    Order_total = int(Order_total)

    return render_template('checkout/checkout.html',
                           Order_total=Order_total, items=items,
                           total=total)


def calculate_order_amount(items):
    Order_total = db.session.query(func.sum(Item.price * (Item.quantity))).filter_by(author=current_user).filter_by(status='Ordered').scalar()
    Order_total = int(Order_total)*100
    return Order_total


@orders.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = json.loads(request.data)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=calculate_order_amount(data['items']),
        currency='mxn')
    try:
        # Send publishable key and PaymentIntent details to client
        return jsonify({'publishableKey': publishable_key, 'clientSecret': intent.client_secret})

    except Exception as e:
        return jsonify(error=str(e)), 403

@orders.route('/success_user_account', methods=['POST'])
def user_account_move_to_payed():
    payed_items = Item.query.filter_by(author=current_user).filter_by(status='Ordered')\
        .update({ Item.status: 'Payed', Item.order_date: datetime.utcnow()})
    db.session.commit()

    return redirect(url_for('users.account'))


@orders.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = 'whsec_ejjoE0BjBWDUrfGmYN92JjNeiiIKjBRn'
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')
        move_to_payed()
        # Fulfill any orders, e-mail receipts, etc
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
    elif event_type == 'payment_intent.payment_failed':
        print('❌ Payment failed.')
    return jsonify({'status': 'success'})


@orders.route('/thanks')
def thanks():
    items = Item.query.filter_by(author=current_user) .order_by(Item.order_date.desc())
    total = db.session.query(func.sum(Item.price)).filter_by(author=current_user).filter_by(status='Ordered').scalar()
    Order_total = db.session.query(func.sum(Item.price * Item.quantity)).filter_by(author=current_user).filter_by(status='Ordered').scalar()

    return render_template('users/thank_you.html', items=items,
                           total=total, Order_total=Order_total)

#################### Action #############################

@orders.route("/cancel_order_items", methods=['GET', 'POST'])
@login_required
def cancel_order():
    order_items = Item.query.filter_by(author=current_user).filter_by(status='Ordered').update({ Item.status: 'Cancel'})
    db.session.commit()

    flash('Su Orden fue Cancelada!', 'danger')
    return redirect(url_for('main.home'))


@orders.route("/order/int:<itemid>", methods=['GET', 'POST'])
@login_required
def ordered_item(itemid):
    cart_item = Item.query.get_or_404(itemid)
    return render_template('order/item_ordered_detail.html', cart_item=cart_item)
