from flask_wtf import FlaskForm
from wtforms import \
    StringField, RadioField, TimeField, BooleanField,\
    SubmitField, PasswordField, IntegerField, FieldList, \
    FormField, SelectField, DateTimeField
from wtforms.fields.html5 import TelField, EmailField, DateField
from wtforms.validators import optional, input_required, equal_to, length, email


class UserForm(FlaskForm):
    username        = StringField('Логин', validators=[input_required(), length(min=3, max=16)])
    password        = PasswordField('Пароль', validators=[input_required(), length(min=4)])
    repeat_password = PasswordField('Повторите пароль', validators=[input_required(), length(min=4)])


class TenantForm(FlaskForm):
    full_name       = StringField('Фамилия, Имя, Отчество', validators=[input_required(), length(min=3, max=16)])
    doc_type        = SelectField('Тип документа', choices=[
        'Паспорт Российской Федерации', 'United States Passport', 'Пасспорт України'
    ])
    doc_number      = StringField('Серия и номер документа', validators=[input_required(), length(min=6)])
    date_of_birth   = DateField('Дата рождения', validators=[input_required()])
    phone           = TelField('Номер телефона', validators=[optional()])
    email           = EmailField('Номер телефона', validators=[optional(), email()])


class RentForm(FlaskForm):
    from app import db
    from app.models import Room
    room_id = RadioField('Номер комнаты', validators=[input_required()])

    end_of_period = DateField('Конец аренды', validators=[input_required()])
