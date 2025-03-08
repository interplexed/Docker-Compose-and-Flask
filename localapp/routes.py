from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db, bcrypt
from .models import User


main = Blueprint("main", __name__)


@main.route('/')
def home():
    if current_user.is_authenticated:
       return redirect(url_for('main.welcome'))
    else:
        return redirect(url_for('main.login'))



@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, email=email, password_hash=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')



@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        flash('test', 'danger')
        user = User.query.filter_by(username=request.form['username']).first()
        #if user and bcrypt.check_password_hash(user.password_hash, request.form['password']):
        if user and user.check_password(request.form['password']):
            flash('OK', 'success')
            login_user(user)
            return redirect(url_for('main.welcome'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')



@main.route('/welcome')
@login_required
def welcome():
    user = User.query.filter(User.id==current_user.id).first()
    return render_template('welcome.html', user=user)



@main.route('/logout')
def logout():
    logout_user()
    flash('You have logged out.', 'info')
    return redirect(url_for('main.login'))
