from apiflask import APIBlueprint

bp = APIBlueprint('main', __name__, tag="main")

@bp.route('/')
def index():
    return {"message": "API működik"}

from app.blueprints.user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix="/user")