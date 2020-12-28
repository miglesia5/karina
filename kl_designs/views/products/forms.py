from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FloatField, StringField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    category = SelectField('Categoria:', coerce=int, id='select_category')
    product_name = StringField('Nombre del Producto:', validators=[DataRequired()])
    description = TextAreaField('Descripcion:', validators=[DataRequired()])
    regular_price = FloatField('Precio:', validators=[DataRequired()])

    Update = SubmitField('Actualizar')

    submit = SubmitField('Agregar')


class UpdateProduct(FlaskForm):
    category_id = SelectField('Categoria:', coerce=int, id='select_category')
    productName = StringField('Nombre del Producto:', validators=[DataRequired()])

    productDescription = TextAreaField('Descripcion:', validators=[DataRequired()])
    productPrice = FloatField('Precio:', validators=[DataRequired()])

    picture = FileField('Foto del Producto', validators=[FileAllowed(['jpg', 'png','gif','jpeg', 'svg'])])
    Update = SubmitField('Actualizar')

    picture2 = FileField('Foto del Producto 2', validators=[FileAllowed(['jpg', 'png','gif','jpeg', 'svg'])])
    Update = SubmitField('Update')

    picture3 = FileField('Foto del Producto 3', validators=[FileAllowed(['jpg', 'png','gif','jpeg', 'svg'])])
    Update = SubmitField('Update')


###################### Carts #########################

class Product_Item_Form(FlaskForm):
    quantity = SelectField('Cantidad',
                        choices=[('1', '1'), ('2', '2'),('3', '3'),('4', '4'),('5', '5'),
                                 ('6', '6'), ('7', '7'),('8', '8'),('9', '9'),('10', '10')])

    ring_size = SelectField('Tamaño',
                        choices=[('1', '1'), ('2', '2'),('3', '3'),('4', '4'),('5', '5'),
                                 ('6', '6'), ('7', '7'),('8', '8'),('9', '9'),('10', '10')])

    submit = SubmitField('Agregar')

