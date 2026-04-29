from app.blueprints.car import bp
from app.blueprints.car.schemas import CarRequestSchema, CarResponseSchema
from app.blueprints.car.service import CarService
from apiflask import HTTPError
from app.extensions import auth
from app.blueprints import role_required

@bp.get('/list')
@bp.output(CarResponseSchema(many=True))
def list_cars():
    success, res = CarService.get_all()
    if success: return res
    raise HTTPError(400, message=res)


@bp.get('/<int:cid>')
@bp.output(CarResponseSchema)
def get_car(cid):
    success, res = CarService.get_one(cid)
    if success: return res
    raise HTTPError(404, message=res)


@bp.post('/add')
@bp.input(CarRequestSchema)
@bp.output(CarResponseSchema)
@bp.auth_required(auth)
@role_required(["ADMIN"])
def add_car(json_data):
    success, res = CarService.add(json_data)
    if success: return res
    raise HTTPError(400, message=res)


@bp.put('/update/<int:cid>')
@bp.input(CarRequestSchema)
@bp.output(CarResponseSchema)
def update_car(cid, json_data):
    success, res = CarService.update(cid, json_data)


@bp.delete('/delete/<int:cid>')
@bp.auth_required(auth)
@role_required(["ADMIN"])
def delete_car(cid):
    success, res = CarService.delete(cid)
    if success: return {"message": res}
    raise HTTPError(400, message=res)