from app.blueprints.rental import bp
from app.blueprints.rental.schemas import RentalCreateSchema, RentalResponseSchema
from app.blueprints.rental.service import RentalService
from apiflask import HTTPError
from app.extensions import auth
from app.blueprints import role_required


@bp.post("/")
@bp.input(RentalCreateSchema)
@bp.output(RentalResponseSchema)
@bp.auth_required(auth)
@role_required(["USER"])
def create_rental(json_data):
    user_id = auth.current_user.get("user_id")
    success, res = RentalService.create_rental(user_id, json_data)
    if success:
        return res
    raise HTTPError(400, message=res)

@bp.get("/")
@bp.output(RentalResponseSchema(many=True))
@bp.auth_required(auth)
@role_required(["ADMIN", "STAFF"])
def get_rentals():
    success, res = RentalService.get_all()
    if success:
        return res
    raise HTTPError(400, message=res)

@bp.get("/<int:rid>")
@bp.output(RentalResponseSchema)
@bp.auth_required(auth)
def get_rental(rid):
    user = auth.current_user
    success, res = RentalService.get_by_id(rid, user)
    if success:
        return res
    raise HTTPError(404, message=res)

@bp.patch("/<int:rid>/approve")
@bp.auth_required(auth)
@role_required(["ADMIN", "STAFF"])
def approve(rid):
    success, res = RentalService.approve(rid)
    if success:
        return res
    raise HTTPError(400, message=res)

@bp.patch("/<int:rid>/reject")
@bp.auth_required(auth)
@role_required(["ADMIN", "STAFF"])
def reject(rid):
    success, res = RentalService.reject(rid)
    if success:
        return res
    raise HTTPError(400, message=res)

@bp.patch("/<int:rid>/start")
@bp.auth_required(auth)
@role_required(["ADMIN", "STAFF"])
def start(rid):
    success, res = RentalService.start(rid)
    if success:
        return res
    raise HTTPError(400, message=res)

@bp.patch("/<int:rid>/close")
@bp.auth_required(auth)
@role_required(["ADMIN", "STAFF"])
def close(rid):
    success, res = RentalService.close(rid)
    if success:
        return res
    raise HTTPError(400, message=res)

@bp.get("/car/<int:cid>/booked")
def get_booked_dates(cid):
    success, res = RentalService.get_booked_dates(cid)
    if success:
        return res
    raise HTTPError(400, message=res)

@bp.get("/my")
@bp.output(RentalResponseSchema(many=True))
@bp.auth_required(auth)
def get_my_rentals():
    user = auth.current_user
    success, res = RentalService.get_my_rentals(user)
    if success:
        return res
    raise HTTPError(400, message=res)

