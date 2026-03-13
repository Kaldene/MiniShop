from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm_password = request.form['confirm_password']

        if not username or not password or not email or not confirm_password:
            flash('Заполните поля', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return redirect(url_for('auth.register'))

        user_by_name = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()

        if user_by_name:
            flash('Пользователь с таким именем существует', 'error')
            return redirect(url_for('auth.register'))

        if user_by_email:
            flash('Пользователь с этой почтой существует', 'error')
            return redirect(url_for('auth.register'))

        try:
            hashed_password = generate_password_hash(password)

            new_user = User(
                username=username,
                password_hash=hashed_password,
                email=email
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash('Пользователь успешно создан', 'success')
            return redirect(url_for('auth.register'))

        except Exception:
            db.session.rollback()
            flash('Произошла ошибка создания пользователя', 'error')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash("Заполните поля", "error")
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Пользователь не найден", "error")
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password_hash, password):
            flash("Неверный пароль", "error")
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        flash("Вы успешно вошли", "success")
        return redirect(url_for('auth.login'))  # потом заменишь на главную

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
