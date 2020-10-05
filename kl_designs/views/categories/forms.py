from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):

    category_name = StringField('Nombre de la Categoria', validators=[DataRequired()])
    picture = FileField('Agregar una foto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'])])
    description = TextAreaField('Descripcion', validators=[DataRequired()])

    submit = SubmitField('Agregar')

class UpdateCategoryForm(FlaskForm):

    category_name = StringField('Nombre del la Categoria', validators=[DataRequired()])
    picture = FileField('Foto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'])])
    description = TextAreaField('Descripcion', validators=[DataRequired()])

    submit = SubmitField('Agregar')
