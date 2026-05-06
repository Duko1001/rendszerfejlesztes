from app.extensions import db
from app.models.rental import Rental
from app.models.user import User
from app.models.car import Car
from app.models.invoice import Invoice
from sqlalchemy import select
from datetime import datetime
from app.blueprints.rental.schemas import RentalResponseSchema
import math

class RentalService:

    @staticmethod
    def create_rental(user_id, data):
        user = db.session.get(User, user_id)
        if not user:
            return False, "User not found"

        car = db.session.get(Car, data["car_id"])
        if not car:
            return False, "Car not found"

        if data["end_time"] < data["start_time"]:
            return False, "Invalid date range"

        existing = db.session.query(Rental).filter(
            Rental.car_id == car.id,
            Rental.start_time < data["end_time"],
            Rental.end_time > data["start_time"]
        ).first()

        if existing:
            return False, "Car already booked"

        rental = Rental(
            user_id=user_id,
            car_id=car.id,
            start_time=data["start_time"],
            end_time=data["end_time"],
            status="PENDING"
        )

        db.session.add(rental)
        db.session.commit()

        return True, rental

    @staticmethod
    def get_all():
        rentals = db.session.execute(select(Rental)).scalars().all()
        return True, rentals

    @staticmethod
    def get_by_id(rid, user):
        rental = db.session.get(Rental, rid)
        if not rental:
            return False, "Not found"

        user_roles = [r["name"] for r in user.get("roles", [])]

        if "ADMIN" in user_roles or "STAFF" in user_roles:
            return True, rental

        if rental.user_id != user.get("user_id"):
            return False, "Forbidden"

        return True, rental

    @staticmethod
    def approve(rid):
        rental = db.session.get(Rental, rid)
        if not rental:
            return False, "Not found"
        rental.status = "APPROVED"
        db.session.commit()
        return True, RentalResponseSchema().dump(rental)

    @staticmethod
    def reject(rid):
        rental = db.session.get(Rental, rid)
        if not rental:
            return False, "Not found"
        rental.status = "REJECTED"
        db.session.commit()
        return True, RentalResponseSchema().dump(rental)

    @staticmethod
    def start(rid):
        rental = db.session.get(Rental, rid)
        if not rental:
            return False, "Not found"
        rental.status = "ACTIVE"
        rental.start_time = datetime.utcnow()
        db.session.commit()
        return True, RentalResponseSchema().dump(rental)

    @staticmethod
    def close(rid):
        rental = db.session.get(Rental, rid)
        if not rental:
            return False, "Not found"

        rental.status = "CLOSED"

        delta = rental.end_time - rental.start_time
        days = math.ceil(delta.total_seconds() / 86400)
        total = days * rental.car.daily_price

        invoice = Invoice(
            rental_id=rental.id,
            amount=total,
            issued_at=datetime.utcnow(),
            paid=False
        )

        db.session.add(invoice)
        db.session.commit()

        return True, {"message": "Closed", "total": total}
        
    @staticmethod
    def get_booked_dates(car_id):
        rentals = db.session.query(Rental).filter(
            Rental.car_id == car_id,
            Rental.status.in_(["PENDING", "APPROVED", "ACTIVE"])
        ).all()

        result = []
        for r in rentals:
            result.append({
                "start_time": r.start_time,
                "end_time": r.end_time
            })

            return True, result


    @staticmethod
    def get_my_rentals(user):
        user_id = user.get("user_id")

        rentals = db.session.query(Rental).filter(
            Rental.user_id == user_id
        ).all()

        return True, rentals



    