from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
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
            flash('Пользователь успешно создан', 'success')
            return redirect(url_for('auth.register'))

        except Exception:
            db.session.rollback()
            flash('Произошла ошибка создания пользователя', 'error')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')
