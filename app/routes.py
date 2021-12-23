from sqlalchemy.exc import SQLAlchemyError

from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from app.models import User, AnonymousUser, Rent, Tenant
from app.forms import RegisterUserForm, LoginUserForm, RentForm

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = AnonymousUser


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    flash('Тестовое плавающее сообщение', category='message')
    return render_template('index.html', current_user=current_user)


@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    from app.data import get_rent_data
    rent = RentForm()
    rent_dto = get_rent_data()

    print(rent_dto.selected_room_ids)
    print(rent_dto.available_room_ids)
    for room in rent.rooms:
        # Заполнение списка доступных комнат
        room.room_id.choices = rent_dto.available_room_ids
        # Заполнение выбранных комнат у жильцов
        # room_id = room.room_id.data
    if rent.update_on_submit():
        pass
    if rent.validate_on_submit():
        rents_db = []
        sess = db.session
        for room in rent.rooms:
            print('ROOM')
            rent_db = Rent(
                    room_id=room.room_id.data,
                    beg_of_period=room.beg_of_period.data,
                    end_of_period=room.end_of_period.data,
                )

            for tenant in rent.tenants:

                # Проверка, доступна ли выбранная комната
                # if not (tenant.room_id.data in rent_dto.available_room_ids):
                #     flash('Данные аппартаменты не доступны для аренды!', category='warning')
                # else:
                if tenant.room_id.data == room.room_id.data:
                    tenant_db = Tenant(
                        user=current_user,
                        full_name=tenant.full_name.data,
                        doc_type=tenant.doc_type.data,
                        doc_number=tenant.doc_number.data,
                        date_of_birth=tenant.date_of_birth.data,
                        phone=tenant.phone.data if tenant.phone.data else None,
                        email=tenant.email.data if tenant.email.data else None,
                    )
                    rent_db.tenant = tenant_db
                    try:
                        sess.add(rent_db)
                        sess.commit()
                        print('ADDED TO DATA BASE!')
                    except SQLAlchemyError as e:
                        print(e)
                        sess.rollback()

        flash('Бронирование прошло успешно!', category='message')
        return redirect('index')
    else:
        flash('errors', category='warning')
        print(rent.errors)
        for room in rent.rooms:
            print('room room id:', type(room.room_id.data), room.room_id.data)
        for tenant in rent.tenants:
            print('tenant room id:', type(tenant.room_id.data), tenant.room_id.data)

        # for room in rent.rooms:
        #     print(room.errors)
        #     for tenant in room.tenants:
        #         print(tenant.errors)
    return render_template('booking.html', rent=rent, rent_dto=rent_dto)


@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginUserForm()
    next = request.args.get('next')

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.from_db(username=username)
        if user:
            user.authenticated = user.check_password(password)
            if user.is_authenticated:
                login_user(user, remember=remember)
                flash(f'Вы успешно вошли! Аккаунт: {username}', category='message')
                return redirect(next if next else url_for('index'))
            else:
                flash('Неверный пароль!', category='warning')
        else:
            flash(f'Пользователя {username} не существует!', category='warning')  # TODO: categories
        print('Form has been validated...')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', category='message')
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterUserForm()
    sess = db.session
    if form.validate_on_submit():
        username = form.user.username.data
        password = form.user.password.data
        user = User.from_db(username=username)
        if user:
            flash(f'Пользователь с логином {username} уже существует!', category='warning')
        else:
            user = User(username=username)
            user.set_password(password)
            sess.add(user)
            sess.commit()
            redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id=None, username=None):
    print('Loading user...')
    user = User.from_db(id=int(user_id), username=username)
    user.authenticated = True
    return user
