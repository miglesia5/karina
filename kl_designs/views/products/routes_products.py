from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required


from kl_designs import db
from kl_designs.models import Category, Product, User
from kl_designs.views.utils import save_picture
from kl_designs.views.products.forms import ProductForm, UpdateProduct, Product_Item_Form

products = Blueprint('products', __name__)


# form.category_id.choices = [(row.id, row.category_name) for row in Category.query.all()]
# image_file = ""  # safer way in case the image is not included in the form

@products.route("/product/new", methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductForm(request.form)
    categories = Category.query.all()
    form.category.choices = [(row.id, row.category_name) for row in Category.query.all()]

    if form.validate_on_submit():
        product = Product(product_name=form.product_name.data,
                          description=form.description.data,
                          price=form.regular_price.data,

                          category_id=form.category.data)


        db.session.add(product)
        db.session.commit()
        flash('El Producto fue Creado!', 'success')
        return redirect(url_for('products.table_products'))

    return render_template('product/register_product.html', title='New Task',
                           form=form, legend='New Product', categories=categories)


@products.route("/product/<int:productid>/update", methods=['GET', 'POST'])
@login_required
def update_product(productid):
    product = Product.query.get_or_404(productid)
    form = UpdateProduct()
    form.category_id.choices = [(row.id, row.category_name) for row in Category.query.all()]
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            product.image_file = picture_file

            picture_file_2 = save_picture(form.picture2.data)
            product.image_file_2 = picture_file_2

            picture_file_3 = save_picture(form.picture3.data)
            product.image_file_3 = picture_file_3

        product.product_name = form.productName.data
        product.description = form.productDescription.data
        product.price = form.productPrice.data


        db.session.commit()

        flash('Su Producto fue Actualizado!', 'success')
        return redirect(url_for('admins.index', productid=productid))

    elif request.method == 'GET':
            form.productName.data = product.product_name
            form.productDescription.data = product.description
            form.productPrice.data = product.price


    image_file = url_for('static', filename='photos/' + current_user.image_file)
    return render_template('product/update_product.html', legend="Update Product", form=form,
                           image_file=image_file, product=product)



@products.route("/delete_product/<int:product_id>/delete", methods=['POST'])
@login_required
def delete_product(product_id):
    product_delete = Product.query.get_or_404(product_id)

    db.session.delete(product_delete)
    db.session.commit()
    flash('Su Producto fue borrado!', 'danger')
    return redirect(url_for('products.table_products'))


@products.route("/all_product")
def all_product():
        products = Product.query.all()
        return render_template('product/all_products.html', products=products)


@products.route("/product/<int:productid>")
def product(productid):
        form = Product_Item_Form()
        product = Product.query.get_or_404(productid)

        return render_template('product/simple_product_details.html', product=product, form=form)


@products.route("/products_table")
def table_products():
    products = Product.query.all()
    product_count = db.session.query(Product.productid).count()

    category_count = db.session.query(Category.id).count()
    user_count = db.session.query(User.id).count()

    return render_template('product/products_table.html',
                               products=products, category_count=category_count,
                               product_count=product_count, user_count=user_count)







