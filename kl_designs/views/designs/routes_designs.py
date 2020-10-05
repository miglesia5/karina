from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required


from kl_designs import db
from kl_designs.models import Product, User, Design
from kl_designs.views.utils import save_picture
from kl_designs.views.designs.forms import DesignForm, UpdateDesignForm

designs = Blueprint('designs', __name__)


@designs.route("/designs/new", methods=['GET', 'POST'])
@login_required
def new_designs():
    form = DesignForm()
    image_file = ""  # safer way in case the image is not included in the form
    if form.validate_on_submit():
        design = Design(design_name=form.design_name.data,
                            image_file=form.picture.data,
                            description=form.description.data)

        db.session.add(design)
        db.session.commit()
        flash('Su Diseño fue Cread0!', 'success')
        return redirect(url_for('admins.index'))

    return render_template('design/create_design.html', title='New Task',
                           form=form, legend='New Category', image_file=image_file)


@designs.route("/design/<int:id>")
def design(id):
        design = Design.query.get_or_404(id)
        image_design = db.session.query(Design.image_file)

        return render_template('design/design_details.html', design=design, image_design=image_design)


@designs.route("/design/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_design(id):
    design = Design.query.get_or_404(id)
    form = UpdateDesignForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            design.image_file = picture_file

        design.design_name = form.design_name.data
        design.description = form.description.data

        db.session.commit()

        flash('La Categoria fue Actualizada!', 'success')
        return redirect(url_for('designs.table_designs'))

    elif request.method == 'GET':
        form.design_name.data = design.design_name
        form.description.data = design.description


    image_file = url_for('static', filename='photos/' + current_user.image_file)
    return render_template('design/update_design.html', title='Update Category',
                          form=form, image_file=image_file, design=design)


@designs.route("/delete_design/<int:id>/delete", methods=['POST'])
@login_required
def delete_design(id):
    design_delete = Design.query.get_or_404(id)

    db.session.delete(design_delete)
    db.session.commit()
    flash('Su Categoria fue Borrada!', 'danger')
    return redirect(url_for('main.home'))


@designs.route("/all_designs")
def all_designs():
        designs = Design.query.all()

        return render_template('design/all_designs.html', designs=designs)

@designs.route("/del_mundo")
def world_designs():

        return render_template('design/world_designs.html', designs=designs)



@designs.route("/designs_table")
@login_required
def table_designs():
        designs = Design.query.all()
        design_count = db.session.query(Design.id).count()

        user_count = db.session.query(User.id).count()
        product_count = db.session.query(Product.productid).count()

        return render_template('design/designs_table.html',
                               designs=designs, design_count=design_count,
                               product_count=product_count, user_count=user_count)
