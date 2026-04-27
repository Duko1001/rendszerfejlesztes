from app.blueprints.rental import bp
from app.blueprints.rental.schemas import RentalCreateSchema, RentalResponseSchema
from app.blueprints.rental.service import RentalService
from apiflask import HTTPError

@bp.post("/")
@bp.input(RentalCreateSchema)
@bp.output(RentalResponseSchema)
def create_rental(json_data):
    success, res = RentalService.create_rental(json_data)
    if success: return res
    raise HTTPError(400, message=res)

@bp.get("/")
@bp.output(RentalResponseSchema(many=True))
def get_rentals():
    return RentalService.get_all()

@bp.get("/<int:rid>")
@bp.output(RentalResponseSchema)
def get_rental(rid):
    res = RentalService.get_by_id(rid)
    if not res:
        raise HTTPError(404, message="Rental not found")
    return res

@bp.patch("/<int:rid>/approve")
def approve(rid):
    success, res = RentalService.approve(rid)
    if success: return res
    raise HTTPError(400, message=res)

@bp.patch("/<int:rid>/reject")
def reject(rid):
    success, res = RentalService.reject(rid)
    if success: return res
    raise HTTPError(400, message=res)

@bp.patch("/<int:rid>/start")
def start(rid):
    success, res = RentalService.start(rid)
    if success: return res
    raise HTTPError(400, message=res)

@bp.patch("/<int:rid>/close")
def close(rid):
    success, res = RentalService.close(rid)
    if success: return res
    raise HTTPError(400, message=res)