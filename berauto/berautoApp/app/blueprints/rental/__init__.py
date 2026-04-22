from apiflask import APIBlueprint

bp = APIBlueprint('rental', __name__, tag="rental")

from app.blueprints.rental import routes