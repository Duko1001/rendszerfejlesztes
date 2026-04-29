from apiflask import APIBlueprint
from app.extensions import auth
from flask import current_app
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError

bp = APIBlueprint('main', __name__, tag="main")

from app.blueprints.user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix='/user')

from app.blueprints.car import bp as car_bp
bp.register_blueprint(car_bp, url_prefix='/car')

from app.blueprints.rental import bp as rental_bp
bp.register_blueprint(rental_bp, url_prefix='/rental')

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(
            token.encode("ascii"),
            current_app.config["SECRET_KEY"]
        )

        if data["exp"] < int(datetime.now().timestamp()):
            return None

        return data
    except:
        return None


def role_required(roles):
    def wrapper(fn):
        def decorated(*args, **kwargs):
            user_roles = [r["name"] for r in auth.current_user.get("roles")]

            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)

            raise HTTPError(403, message="Access denied")
        return decorated
    return wrapper