import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import session, flash, redirect, url_for
from flask_security.forms import Email
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, RadioField




class CartForm(FlaskForm):
    productid = SelectField('Categoria:', coerce=int, id='select_category')
    quantity = SelectField('Cantidad',
                        choices=[('1', '1'), ('2', '2'),('3', '3'),('4', '4'),('5', '5'),
                                 ('6', '6'), ('7', '7'),('8', '8'),('9', '9'),('10', '10')])

    submit = SubmitField('Agregar')



class UpdateCartForm(FlaskForm):
    productid = SelectField('Categoria:', coerce=int, id='select_category')
    quantity = SelectField('Cantidad',
                        choices=[('1', '1'), ('2', '2'),('3', '3'),('4', '4'),('5', '5'),
                                 ('6', '6'), ('7', '7'),('8', '8'),('9', '9'),('10', '10')])

    submit = SubmitField('Update')

