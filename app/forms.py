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
    room_id         = SelectField('Номер комнаты', choices=[], validators=[input_required()])
    full_name       = StringField('Фамилия, Имя, Отчество', validators=[input_required(), length(min=3, max=16)])
    doc_type        = SelectField('Тип документа', choices=[
        'Паспорт Российской Федерации', 'United States Passport', 'Пасспорт України'
    ])
    doc_number      = StringField('Серия и номер документа', validators=[input_required(), length(min=6)])
    date_of_birth   = DateField('Дата рождения', validators=[input_required()])
    phone           = TelField('Номер телефона', validators=[optional()])
    email           = EmailField('Номер телефона', validators=[optional(), email()])

    def add_room_id(self, room_id):
        self.room_id.choices.append(room_id)


class RoomForm(FlaskForm):
    from app import db
    from app.models import Room
    room_id         = RadioField('Номер комнаты', choices=[], validators=[input_required()])
    beg_of_period   = DateField('Начало аренды', validators=[input_required()])
    end_of_period   = DateField('Конец аренды', validators=[input_required()])


class RentForm(FlaskForm):
    rooms           = FieldList(FormField(RoomForm))
    tenants         = FieldList(FormField(TenantForm))

    btn_add_room    = SubmitField('Добавить номер')
    btn_add_tenant = SubmitField('Добавить жильца')

    btn_submit      = SubmitField('Забронировать')

    def add_room(self):
        self.rooms.append_entry()

    def add_tenant(self):
        self.tenants.append_entry()

    def update_on_submit(self):

        if self.btn_add_room.data:
            self.add_room()
            return self.btn_add_room
        elif self.btn_add_tenant.data:
            self.add_tenant()
            return self.btn_add_tenant
        else: return False


class RegisterUserForm(FlaskForm):
    user            = FormField(UserForm)

    btn_register    = SubmitField('Зарегистрироваться')


class LoginUserForm(FlaskForm):
    username = StringField('Логин', validators=[input_required(), length(min=3, max=16)])
    password = PasswordField('Пароль', validators=[input_required(), length(min=4)])

    remember = BooleanField('Не выходить из аккаунта')
    btn_login = SubmitField('Войти')
