from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class AnilloForm(FlaskForm):

    anillo_compromiso_name = StringField('Nombre del Anillo de Compromiso', validators=[DataRequired()])
    picture = FileField('Agregar una foto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'])])

    submit = SubmitField('Agregar')

class UpdateAnilloForm(FlaskForm):

    anillo_compromiso_name = StringField('Nombre del Anillo de Compromiso', validators=[DataRequired()])
    picture = FileField('Foto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'])])

    submit = SubmitField('Agregar')
