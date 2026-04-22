from apiflask import APIBlueprint

bp = APIBlueprint('main', __name__, tag="main")

@bp.route('/')
def index():
    return {"message": "API működik"}

from app.blueprints.user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix="/user")

from app.blueprints.rental import bp as rental_bp
bp.register_blueprint(rental_bp, url_prefix="/rental")