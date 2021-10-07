from kl_designs import db
from kl_designs.models import User, Product, Category, Design
from flask import render_template, Blueprint


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    users = User.query.all()
    user_count = db.session.query(User.id).count()

    categories = Category.query.all()
    designs = Design.query.all()

    return render_template('main/home.html',
                           user_count=user_count, users=users,
                           categories=categories,
                           designs=designs)

################ Category Products########################

@main.route("/category/<category_name>")
def product_category(category_name):
    category = Category.query.filter_by(category_name=category_name).first_or_404()
    products = Product.query.filter_by(line=category)

    return render_template('product/products.html', category=category,
                           products=products)
