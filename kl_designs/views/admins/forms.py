from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from kl_designs.models import User


class Delivery_Form(FlaskForm):
    deliveryid = StringField('Insert Delivery Number', validators=[DataRequired()])
    carrier = StringField("""Add Carrier's Name:""", validators=[DataRequired()])
    submit = SubmitField('Submit')


class Received_Form(FlaskForm):
    deliveryid = StringField('Insert Delivery Number', validators=[DataRequired()])
    carrier = StringField("""Add Carrier's Name:""", validators=[DataRequired()])
    submit = SubmitField('Submit')


class Admin_Update_User_AccountForm(FlaskForm):
    fname = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    complete_address1 = StringField('Direccion Completa', validators=[DataRequired(), Length(min=1, max=100)])

    zipcode = StringField('Codigo Posta', validators=[DataRequired(), Length(min=1, max=15)])
    phone = StringField('Telefono', validators=[DataRequired(), Length(min=1, max=100)])

    password = StringField('Contraseña', validators=[DataRequired()])

    picture = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Cuidado')