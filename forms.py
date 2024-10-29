from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange
from models import User, Category, Product
from flask_login import current_user
from wtforms import FileField

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('Имя')
    last_name = StringField('Фамилия')
    phone = StringField('Телефон')
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким email уже существует.')
        

class UpdateProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Имя')
    last_name = StringField('Фамилия')
    phone = StringField('Телефон')
    submit = SubmitField('Сохранить')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Пользователь с таким email уже существует.')

# Формы для менеджера

class AddProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    category_id = SelectField('Категория', coerce=int, choices=[], validators=[DataRequired()])
    image = FileField('Изображение')
    submit = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

class EditProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    category_id = SelectField('Категория', coerce=int, choices=[], validators=[DataRequired()])
    image = FileField('Изображение')
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

class AddCategoryForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])

    submit = SubmitField('Добавить')


class EditCategoryForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    
    submit = SubmitField('Сохранить')


class OrderForm(FlaskForm):
    address = StringField('Адрес доставки', validators=[DataRequired()])
    payment_method = SelectField('Способ оплаты', choices=[('Наложенный платеж', 'Наложенный платеж')], default='Наложенный платеж')
    submit = SubmitField('Оформить заказ')