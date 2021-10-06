from werkzeug.security import generate_password_hash
from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app import forms
from flask_login import current_user, login_user, login_required, logout_user


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
