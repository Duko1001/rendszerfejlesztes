from apiflask import APIBlueprint
bp = APIBlueprint('car', __name__, tag="car")
from app.blueprints.car import routes