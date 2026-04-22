from app.blueprints.rental import bp
from app.blueprints.rental.schemas import RentalCreateSchema, RentalResponseSchema
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