import os
import secrets

from PIL import Image
from flask import url_for, request
from flask_mail import Message
from kl_designs import mail
from kl_designs import app_root


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app_root, 'static/photos/', picture_fn)

    output_size = (3024, 4032)
    i = Image.open(form_picture)
    rgb_i = i.convert('RGB')
    rgb_i.thumbnail(output_size)
    rgb_i.save(picture_path)

    return picture_fn


def upload_image(form_picture):
    target = os.path.join(app_root, 'photos/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_cancel_email(order_items, author):
    msg = Message('Order Cancellation',
                  sender='estudiokarinaloranca@gmail.com',
                  recipients=['estudiokarinaloranca@gmail.com'])
    msg.body = f'''The Order for {order_items, author} Has been Cancel'''
    mail.send(msg)

def send_order_email(order_items, author):
    msg = Message('Order Request',
                  sender='estudiokarinaloranca@gmail.com',
                  recipients=['estudiokarinaloranca@gmail.com'])
    msg.body = f'''An Order has been made for {order_items, author}'''
    mail.send(msg)

def send_payed_email(itemid, author):
    msg = Message('Order Request',
                  sender='estudiokarinaloranca@gmail.com',
                  recipients=['estudiokarinaloranca@gmail.com'])
    msg.body = f'''{itemid} for {author} have been payed'''
    mail.send(msg)


def send_sent_email(itemid, author):
    msg = Message('Order Request',
                  sender='estudiokarinaloranca@gmail.com',
                  recipients=['estudiokarinaloranca@gmail.com'])
    msg.body = f'''{itemid} for {author} have been sent'''
    mail.send(msg)
