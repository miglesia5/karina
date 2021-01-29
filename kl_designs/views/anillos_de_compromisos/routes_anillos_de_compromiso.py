from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required

from kl_designs import db
from kl_designs.models import Product, User, AnillosCompromiso
from kl_designs.views.anillos_de_compromisos.forms import AnilloForm, UpdateAnilloForm
from kl_designs.views.utils import save_picture

anillos = Blueprint('anillos', __name__)


@anillos.route("/anillos/new", methods=['GET', 'POST'])
@login_required
def new_anillos():
    form = AnilloForm()
    image_file = ""  # safer way in case the image is not included in the form
    if form.validate_on_submit():
        anillo = AnillosCompromiso(anillo_compromiso_name=form.anillo_compromiso_name.data,
                                   image_file=form.picture.data)

        db.session.add(anillo)
        db.session.commit()
        flash('Su Anillo de Compromiso fue Creado!', 'success')
        return redirect(url_for('admins.index'))

    return render_template('anillo/create_anillo.html',
                           form=form, image_file=image_file)


@anillos.route("/anillo/<int:id>")
def anillo(id):
        anillo = AnillosCompromiso.query.get_or_404(id)
        image_anillo = db.session.query(AnillosCompromiso.image_file)

        return render_template('anillo/anillo_details.html', anillo=anillo, image_anillo=image_anillo)


@anillos.route("/anillo/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_anillo(id):
    anillo = AnillosCompromiso.query.get_or_404(id)
    form = UpdateAnilloForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            anillo.image_file = picture_file

        anillo.anillo_compromiso_name = form.anillo_compromiso_name.data

        db.session.commit()

        flash('El Anillo de Compromiso fue Actualizado!', 'success')
        return redirect(url_for('anillos.table_anillos'))

    elif request.method == 'GET':
        form.anillo_compromiso_name.data = anillo.anillo_compromiso_name

    image_file = url_for('static', filename='photos/' + current_user.image_file)
    return render_template('anillo/update_anillo.html',
                          form=form, image_file=image_file, anillo=anillo)


@anillos.route("/delete_anillo/<int:id>/delete", methods=['POST'])
@login_required
def delete_anillo(id):
    anillo_delete = AnillosCompromiso.query.get_or_404(id)

    db.session.delete(anillo_delete)
    db.session.commit()
    flash('Su Anillo de Compromiso fue Borrado!', 'danger')
    return redirect(url_for('anillos.table_anillos'))


@anillos.route("/anillos_del_mundo")
def world_anillos():
        anillos = AnillosCompromiso.query.all()
        return render_template('anillo/world_anillos.html', anillos=anillos)


@anillos.route("/anillos_table")
@login_required
def table_anillos():
        anillos = AnillosCompromiso.query.all()
        anillos_count = db.session.query(AnillosCompromiso.id).count()

        user_count = db.session.query(User.id).count()
        product_count = db.session.query(Product.productid).count()

        return render_template('anillo/anillos_table.html',
                               anillos=anillos, anillos_count=anillos_count,
                               product_count=product_count, user_count=user_count)
