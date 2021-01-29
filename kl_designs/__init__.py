import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from kl_designs.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
app_root = os.path.dirname(os.path.abspath(__file__))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from kl_designs.views.main.routes_main import main
    from kl_designs.views.admins.routes_admins import admins
    from kl_designs.views.users.routes_users import users

    from kl_designs.views.categories.routes_categories import categories
    from kl_designs.views.products.routes_products import products

    from kl_designs.views.designs.routes_designs import designs
    from kl_designs.views.taller.routes_taller import tallers
    from kl_designs.views.anillos_de_compromisos.routes_anillos_de_compromiso import anillos

    from kl_designs.views.orders.routes_orders import orders
    from kl_designs.views.carts.routes_carts import carts

    app.register_blueprint(main)
    app.register_blueprint(admins)
    app.register_blueprint(users)

    app.register_blueprint(categories)
    app.register_blueprint(products)

    app.register_blueprint(designs)
    app.register_blueprint(tallers)
    app.register_blueprint(anillos)

    app.register_blueprint(carts)
    app.register_blueprint(orders)

    return app
