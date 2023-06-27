from SSS import app

from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash
import os

from datetime import datetime
import pytz

import re

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=False, primary_key=False)
    password = db.Column(db.String(16))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def isalnum_ascii(s):
    return True if s.isalnum() and s.isascii() else False

@app.route("/", methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'GET':
        posts  = User.query.all()
        current_user.id = f'{current_user.id:08}'
        return render_template('schedule.html', posts=posts, current_user=current_user)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if(len(username) > 16):
            e = 'ユーザ名は16文字以内にしてください'
            return render_template('signup.html', e=e)
        if(len(password) > 16):
            e = 'パスワードは16文字以内にしてください'
            return render_template('signup.html', e=e)
        r = isalnum_ascii(password)
        if(f'{password} isalnum_ascii: {r}' == False):
            e = 'パスワードは半角英数にしてください'
            return render_template('signup.html', e=e)
        user = User(username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect('/')
    else:
        return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hage = request.args.get('checkbox_sample', default='', type=str)
        if hage == 'on':
            return render_template('signup.html')
        id = request.form.get('id')
        password = request.form.get('password')

        if(User.query.filter_by(id=id).count()==0):
            e = 'IDが間違っています'
            return render_template('login.html', e=e)

        user = User.query.filter_by(id=id).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            e = 'IDまたはパスワードが間違っています'
            return render_template('login.html', e=e)
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
