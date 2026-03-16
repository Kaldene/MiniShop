from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
from models import db, User,Role

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        confirm_password = request.form.get('confirm_password', '')

        if not username or not password or not email or not confirm_password:
            flash('Заполните все поля', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('auth.register'))

        user_by_name = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()

        if user_by_name:
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('auth.register'))

        if user_by_email:
            flash('Пользователь с этой почтой уже существует', 'danger')
            return redirect(url_for('auth.register'))

        role = Role.query.filter_by(name='user').first()
        if not role:
            flash('Роль user не найдена', 'danger')
            return redirect(url_for('auth.register'))

        try:
            hashed_password = generate_password_hash(password)

            new_user = User(
                username=username,
                password_hash=hashed_password,
                email=email,
                role_id=role.id
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash('Пользователь успешно создан', 'success')
            return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()
            print('Ошибка регистрации:', e)
            flash('Произошла ошибка при создании пользователя', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Заполните все поля', 'danger')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Пользователь не найден', 'danger')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password_hash, password):
            flash('Неверный пароль', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        flash('Вы успешно вошли', 'success')
        return redirect(url_for('main.home'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('auth.login'))