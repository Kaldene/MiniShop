from flask import Flask
from config import Config
from models import db, User, Role
from flask_login import LoginManager
from routes.auth.routes import auth_bp
from routes.main.main import main_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if not Role.query.filter_by(name='admin').first():
            admin_role = Role(name='admin')
            db.session.add(admin_role)

        if not Role.query.filter_by(name='user').first():
            user_role = Role(name='user')
            db.session.add(user_role)

        db.session.commit()

    app.run(debug=True)