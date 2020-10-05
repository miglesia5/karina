from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func

from kl_designs import db, bcrypt
from kl_designs.models import User, Item
from kl_designs.views.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm

from kl_designs.views.utils import save_picture, send_reset_email





users = Blueprint('users', __name__)


@users.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data, email=form.email.data,
                    complete_address1=form.complete_address1.data,
                    zipcode=form.zipcode.data, phone=form.phone.data,
                    password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash('Tu Cuenta fue creada ahora puede iniciar tu sesion', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('No se pudo iniciar sesion. Por favor revisa el mail y contraseña o registrate si no lo hiciste todavia  ', 'danger')
    return render_template('users/login.html', title='Login', form=form)



@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    items = Item.query.filter_by(author=current_user) .order_by(Item.order_date.desc())
    total = db.session.query(func.sum(Item.price)).filter_by(author=current_user).filter_by(status='Ordered').scalar()
    Order_total = db.session.query(func.sum(Item.price * Item.quantity)).filter_by(author=current_user).filter_by(status='Ordered').scalar()

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.fname = form.fname.data
        current_user.email = form.email.data

        current_user.complete_address1 = form.complete_address1.data
        current_user.zipcode = form.zipcode.data
        current_user.phone = form.phone.data

        db.session.commit()
        flash('Tu Cuenta ha sido actualizada!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.fname.data = current_user.fname
        form.email.data = current_user.email
        form.complete_address1.data = current_user.complete_address1
        form.zipcode.data = current_user.zipcode
        form.phone.data = current_user.phone

    image_file = url_for('static', filename='photos/' + current_user.image_file)
    return render_template('users/account.html', title='Account',
                           image_file=image_file, form=form,
                           items=items, total=total, Order_total=Order_total
                           )




###################### RESETS ####################################


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Un mail ha sido enviado con instrucciones para resetear tu cuenta', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Ese es un Token Invalido', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Tu Contraseña fue actualizada! Ya puede iniciar sesion', 'success')
        return redirect(url_for('users.login'))
        return render_template('users/reset_token.html', title='Reset Password', form=form)


