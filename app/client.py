from flask import Blueprint, render_template
from flask_security import auth_required

bp = Blueprint('client', __name__, url_prefix='/client')


@bp.route("/")
@auth_required()
def index():
    return render_template('client/index.html')
