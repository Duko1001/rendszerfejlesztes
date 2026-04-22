from app.blueprints.rental import bp
from app.blueprints.rental.schemas import (
    RentalCreateSchema,
    RentalResponseSchema,
    CloseRentalResponseSchema
)
from app.blueprints.rental.service import RentalService
from apiflask import HTTPError


@bp.post("/")
@bp.input(RentalCreateSchema, location="json")
@bp.output(RentalResponseSchema)
def create_rental(json_data):
    success, response = RentalService.create_rental(json_data)
    if success:
        return response
    raise HTTPError(400, message=response)


@bp.get("/")
@bp.output(RentalResponseSchema(many=True))
def get_rentals():
    return RentalService.get_all()


@bp.get("/<int:rental_id>")
@bp.output(RentalResponseSchema)
def get_rental(rental_id):
    rental = RentalService.get_by_id(rental_id)
    if not rental:
        raise HTTPError(404, message="Rental not found")
    return rental


@bp.get("/user/<int:user_id>")
@bp.output(RentalResponseSchema(many=True))
def get_user_rentals(user_id):
    return RentalService.get_by_user(user_id)


@bp.patch("/<int:rental_id>/approve")
def approve_rental(rental_id):
    success, response = RentalService.approve_rental(rental_id)
    if success:
        return response
    raise HTTPError(400, message=response)


@bp.patch("/<int:rental_id>/reject")
def reject_rental(rental_id):
    success, response = RentalService.reject_rental(rental_id)
    if success:
        return response
    raise HTTPError(400, message=response)


@bp.patch("/<int:rental_id>/start")
def start_rental(rental_id):
    success, response = RentalService.start_rental(rental_id)
    if success:
        return response
    raise HTTPError(400, message=response)


@bp.patch("/<int:rental_id>/close")
@bp.output(CloseRentalResponseSchema)
def close_rental(rental_id):
    success, response = RentalService.close_rental(rental_id)
    if success:
        return response
    raise HTTPError(400, message=response)


@bp.get("/<int:rental_id>/invoice")
def get_invoice(rental_id):
    success, response = RentalService.get_invoice(rental_id)
    if success:
        return response
    raise HTTPError(404, message=response)