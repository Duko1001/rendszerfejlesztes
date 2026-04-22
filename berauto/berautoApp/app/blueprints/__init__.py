from apiflask import APIBlueprint

bp = APIBlueprint('main', __name__, tag="main")

from app.blueprints.user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix='/user')

from app.blueprints.car import bp as car_bp
bp.register_blueprint(car_bp, url_prefix='/car')

from app.blueprints.rental import bp as rental_bp
bp.register_blueprint(rental_bp, url_prefix='/rental')