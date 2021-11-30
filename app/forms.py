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


class RoomForm(FlaskForm):
    from app import db
    from app.models import Room
    tenants         = FieldList(FormField(TenantForm))
    room_id         = RadioField('Номер комнаты', choices=[(i, 'pipa') for i in range(10)], validators=[input_required()])
    beg_of_period   = DateField('Начало аренды')
    end_of_period   = DateField('Конец аренды', validators=[input_required()])

    btn_add_tenant = SubmitField('Добавить жильца')

    def add_tenant(self):
        self.tenants.append_entry()

    def update_on_submit(self):
        if self.btn_add_tenant.data:
            self.add_tenant()
            return self.btn_add_tenant
        else: return False


class RentForm(FlaskForm):
    rooms            = FieldList(FormField(RoomForm))
    btn_add_room    = SubmitField('Добавить номер')

    def add_room(self):
        self.rooms.append_entry()

    def update_on_submit(self):
        if self.btn_add_room.data:
            self.add_room()
            return self.btn_add_room
        else:
            for room in self.rooms:
                return room.update_on_submit()


class RegisterForm(FlaskForm):
    user            = FormField(UserForm)
    rents           = FieldList(FormField(RentForm))

    btn_add_rent    = SubmitField('Забронировать номер')
    btn_register    = SubmitField('Зарегистрироваться')

    def add_rent(self):
        self.rents.append_entry()

    def update_on_submit(self):
        if self.btn_add_rent.data:
            self.add_rent()
            return self.btn_add_rent
        else:
            for rent in self.rents:
                return rent.update_on_submit()
