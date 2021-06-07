from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required


from kl_designs import db
from kl_designs.models import Product, User, Taller
from kl_designs.views.taller.forms import TallerForm, UpdateTallerForm
from kl_designs.views.utils import save_picture


tallers = Blueprint('tallers', __name__)


@tallers.route("/tallers/new", methods=['GET', 'POST'])
@login_required
def new_tallers():
    form = TallerForm()
    image_file = ""  # safer way in case the image is not included in the form
    if form.validate_on_submit():
        taller = Taller(taller_name=form.taller_name.data,
                            image_file=form.picture.data,
                            )

        db.session.add(taller)
        db.session.commit()
        flash('Su Taller fue Creado!', 'success')
        return redirect(url_for('admins.index'))

    return render_template('taller/create_taller.html', title='New Task',
                           form=form, image_file=image_file)


@tallers.route("/taller/<int:id>")
def taller(id):
        taller = Taller.query.get_or_404(id)
        image_taller = db.session.query(Taller.image_file)

        return render_template('taller/taller_details.html', taller=taller, image_taller=image_taller)


@tallers.route("/taller/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_taller(id):
    taller = Taller.query.get_or_404(id)
    form = UpdateTallerForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            taller.image_file = picture_file

        taller.taller_name = form.taller_name.data

        db.session.commit()

        flash('La foto de Taller fue Actualizada!', 'success')
        return redirect(url_for('tallers.table_tallers'))

    elif request.method == 'GET':
        form.taller_name.data = taller.taller_name

    image_file = url_for('static', filename='photos/' + current_user.image_file)
    return render_template('taller/update_taller.html', form=form, image_file=image_file, taller=taller)


@tallers.route("/delete_taller/<int:id>/delete", methods=['POST'])
@login_required
def delete_taller(id):
    taller_delete = Taller.query.get_or_404(id)

    db.session.delete(taller_delete)
    db.session.commit()
    flash('La Foto del Taller fue Borrada!', 'danger')
    return redirect(url_for('tallers.table_tallers'))


@tallers.route("/taller_del_mundo")
def world_tallers():
        tallers = Taller.query.all()
        return render_template('taller/world_tallers.html', tallers=tallers)


@tallers.route("/tallers_table")
@login_required
def table_tallers():
        tallers = Taller.query.all()
        taller_count = db.session.query(Taller.id).count()

        user_count = db.session.query(User.id).count()
        product_count = db.session.query(Product.productid).count()

        return render_template('taller/tallers_table.html',
                               tallers=tallers, taller_count=taller_count,
                               product_count=product_count, user_count=user_count)
