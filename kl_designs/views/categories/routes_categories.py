from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required


from kl_designs import db
from kl_designs.models import Category, Product, User, Design
from kl_designs.views.utils import save_picture
from kl_designs.views.categories.forms import CategoryForm, UpdateCategoryForm

categories = Blueprint('categories', __name__)


@categories.route("/category/new", methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    image_file = ""  # safer way in case the image is not included in the form
    if form.validate_on_submit():
        category = Category(category_name=form.category_name.data,
                            image_file=form.picture.data,
                            description=form.description.data)

        db.session.add(category)
        db.session.commit()
        flash('Su Categoria fue Creada!', 'success')
        return redirect(url_for('categories.table_categories'))

    return render_template('category/create_category.html', title='New Task',
                           form=form, legend='New Category', image_file=image_file)


@categories.route("/category/<int:id>")
def category(id):
        category = Category.query.get_or_404(id)
        image_category = db.session.query(Category.image_file)

        return render_template('category/category_details.html', category=category, image_category=image_category)


@categories.route("/category/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = Category.query.get_or_404(id)
    form = UpdateCategoryForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            category.image_file = picture_file

        category.category_name = form.category_name.data
        category.description = form.description.data

        db.session.commit()

        flash('La Categoria fue Actualizada!', 'success')
        return redirect(url_for('categories.table_categories'))

    elif request.method == 'GET':
        form.category_name.data = category.category_name
        form.description.data = category.description


    image_file = url_for('static', filename='photos/' + current_user.image_file)
    return render_template('category/update_category.html', title='Update Category',
                          form=form, image_file=image_file, category=category)


@categories.route("/delete_category/<int:id>/delete", methods=['POST'])
@login_required
def delete_category(id):
    category_delete = Category.query.get_or_404(id)

    db.session.delete(category_delete)
    db.session.commit()
    flash('Su Categoria fue Borrada!', 'danger')
    return redirect(url_for('categories.table_categories'))


@categories.route("/all_categories")
def all_categories():
        categories = Category.query.all()

        return render_template('category/all_categories.html', categories=categories)



@categories.route("/categories_table")
def table_categories():
        categories = Category.query.all()
        design_count = db.session.query(Design.id).count()

        user_count = db.session.query(User.id).count()
        product_count = db.session.query(Product.productid).count()



        return render_template('category/categories_table.html',
                               categories=categories, design_count=design_count,
                               product_count=product_count, user_count=user_count)
