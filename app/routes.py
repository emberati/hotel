from werkzeug.security import generate_password_hash
from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app import forms
from flask_login import current_user, login_user, login_required, logout_user


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    from app.forms import RegisterForm
    form = RegisterForm()

    updated = form.update_on_submit()
    if updated:
        print('Form is updated', updated)
        pass
    elif form.validate_on_submit():
        print('Form has been validated...')

    return render_template('index.html', form=form)
