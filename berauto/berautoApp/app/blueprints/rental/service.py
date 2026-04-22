from app.extensions import db
from app.models.rental import Rental
from app.models.user import User
from app.models.car import Car
from app.blueprints.rental.schemas import RentalResponseSchema
from sqlalchemy import select

class RentalService:

    @staticmethod
    def create_rental(data):
        user = db.session.execute(select(User).filter_by(id=data["user_id"])).scalar_one_or_none()
        if not user:
            return False, "User not found"

        car = db.session.execute(select(Car).filter_by(id=data["car_id"])).scalar_one_or_none()
        if not car:
            return False, "Car not found"

        if not car.is_available:
            return False, "Car is not available"

        if data["end_time"] < data["start_time"]:
            return False, "Invalid date range"

        rental = Rental(
            user_id=data["user_id"],
            car_id=data["car_id"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            status="PENDING"
        )

        car.is_available = False

        db.session.add(rental)
        db.session.commit()

        return True, RentalResponseSchema().dump(rental)

    @staticmethod
    def get_all():
        rentals = db.session.execute(select(Rental)).scalars().all()
        return RentalResponseSchema(many=True).dump(rentals)

    @staticmethod
    def get_by_id(rental_id):
        rental = db.session.get(Rental, rental_id)
        if not rental:
            return None
        return RentalResponseSchema().dump(rental)