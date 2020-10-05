from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from kl_designs.models import User


class RegistrationForm(FlaskForm):
    fname = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    complete_address1 = StringField('Direccion Completa', validators=[DataRequired(), Length(min=1, max=100)])

    zipcode = StringField('Codigo Postal', validators=[DataRequired(), Length(min=1, max=15)])
    phone = StringField('Telefono', validators=[DataRequired(), Length(min=1, max=100)])

    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Iniciar')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('El mail indicado ya fue utilizado por alguien mas. Por favor elija otro')


class LoginForm(FlaskForm):
    email = StringField('e-mail', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuerdame')
    submit = SubmitField('Iniciar')


class UpdateAccountForm(FlaskForm):
    fname = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    complete_address1 = StringField('Direccion Completa', validators=[DataRequired(), Length(min=1, max=100)])

    zipcode = StringField('Codigo Posta', validators=[DataRequired(), Length(min=1, max=15)])
    phone = StringField('Telefono', validators=[DataRequired(), Length(min=1, max=100)])

    picture = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('De Acuerdo')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('El mail indicado ya fue utilizado por alguien mas. Por favor elija otro.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No existe una cuenta con el email, debes registrarte primero.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('De Acuerdo')
