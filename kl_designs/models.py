from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from kl_designs import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    fname = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String, default='user')

    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    complete_address1 = db.Column(db.String(200), unique=False, nullable=False)
    zipcode = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    cart_items = db.relationship('Item', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='contributor', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.fname}', " \
               f"'{self.complete_address1}'," \
               f"'{self.zipcode}','{self.email}','{self.phone}')"


class Item(db.Model):
    __table_args__ = {'extend_existing': True}
    itemid = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=True)
    size = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String, default='pending')

    product_name = db.Column(db.String(100), nullable=True)
    category_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    price = db.Column(db.DECIMAL)

    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    image_file_2 = db.Column(db.String(20), nullable=True, default='default.jpg')
    image_file_3 = db.Column(db.String(20), nullable=True, default='default.jpg')

    order_date = db.Column(db.DateTime, nullable=True)
    delivery_date = db.Column(db.DateTime, nullable=True)
    received_date = db.Column(db.DateTime, nullable=True)

    deliveryid = db.Column(db.Integer, nullable=True)
    carrier = db.Column(db.String(100), nullable=True)

    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    users = db.relationship(User)
    product_items = db.relationship('Product', backref='product_item', lazy=True)

    def __repr__(self):
        return f"Item('{self.itemid}, '{self.quantity}', '{self.status}', '{self.size}')"


class Category(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    products = db.relationship('Product', backref='line', lazy=True)

    def __repr__(self):
        return f"Category('{self.category_name}')"


class Product(db.Model):
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['name', 'desc']

    productid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.DECIMAL)

    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    image_file_2 = db.Column(db.String(20), nullable=True, default='default.jpg')
    image_file_3 = db.Column(db.String(20), nullable=True, default='default.jpg')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.itemid'), nullable=True)
    item = relationship("Item", back_populates="products")


    comments = db.relationship('Comments', backref='feedback', lazy=True)

    def __repr__(self):
        return f"Product('{self.productid}','{self.product_name}','{self.description}', '{self.image_file}',  '{self.quantity}', '{self.regular_price}', '{self.discounted_price}')"

Item.products = relationship("Product", order_by=Product.productid, back_populates="item")


class Design(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    design_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"Design('{self.design_name}')"



class Comments(db.Model):
    __table_args__ = {'extend_existing': True}

    commentid = db.Column(db.Integer, primary_key=True)
    comment_date = db.Column(db.DateTime, nullable=False)
    product_review = db.Column(db.String(100), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=True)

    def __repr__(self):
        return f"Comments('{self.commentid}', '{self.comment_date}','{self.product_review}'')"

