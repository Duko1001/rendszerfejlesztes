from app.extensions import db
from app.models.rental import Rental
from app.models.user import User
from app.models.car import Car
from app.models.invoice import Invoice
from sqlalchemy import select
from datetime import datetime

class RentalService:

    @staticmethod
    def create_rental(data):

        user = db.session.get(User, data["user_id"])
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
            return False, "Car already booked for this period"

        rental = Rental(
            user_id=data["user_id"],
            car_id=data["car_id"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            status="PENDING"
        )

        db.session.add(rental)
        db.session.commit()

        return True, rental

    @staticmethod
    def get_all():
        return db.session.execute(select(Rental)).scalars().all()

    @staticmethod
    def get_by_id(rid):
        return db.session.get(Rental, rid)

    @staticmethod
    def approve(rid):
        rental = db.session.get(Rental, rid)
        if not rental:
            return False, "Not found"
        rental.status = "APPROVED"
        db.session.commit()
        return True, rental

    @staticmethod
    def reject(rid):
        rental = db.session.get(Rental, rid)
        if not rental:
            return False, "Not found"
        rental.status = "REJECTED"
        rental.car.is_available = True
        db.session.commit()
        return True, rental

    @staticmethod
    def start(rid):
        rental = db.session.get(Rental, rid)
        if not rental:
            return False, "Not found"
        rental.status = "ACTIVE"
        rental.start_time = datetime.utcnow()
        db.session.commit()
        return True, rental

    @staticmethod
    def close(rid):
        rental = db.session.get(Rental, rid)
        if not rental:
            return False, "Not found"

        rental.status = "CLOSED"
        rental.car.is_available = True

        delta = rental.end_time - rental.start_time
        days = max(delta.days, 1)
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