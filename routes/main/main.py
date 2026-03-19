from flask import Blueprint,render_template
from flask_login import login_required, current_user, login_user, logout_user
from models import Review

main_bp = Blueprint('main', __name__)


@main_bp.route('/home')
@main_bp.route('/')
def home():
    reviews = Review.query.order_by(Review.created_at.desc()).limit(3).all()
    return render_template('main/index.html', reviews=reviews)

@main_bp.route('/steam-topup')
def steam_topup():
    return render_template('main/steam_topup.html')