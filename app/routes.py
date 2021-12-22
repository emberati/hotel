from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app import forms
from app import login_manager
from flask_login import current_user, login_required, login_user, logout_user

from app.models import User
from app.forms import RegisterUserForm, LoginUserForm


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #username = current_user.username
    #id = current_user.get_id()
    return render_template('index.html')#, username=username, id=id)


@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    return '<h1>Test booking page</h1>'


@app.route('/statistics')
def statistics():
    return '<h1>Test statistics page</h1>'


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
                redirect(next if next else url_for('booking'))
                flash('Вы успешно вошли!', category='message')
            else:
                flash('Неверный пароль!',  category='warning')
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
