from app.extensions import db
from app.models.rental import Rental
from app.models.invoice import Invoice
from app.models.user import User
from app.models.car import Car
from app.blueprints.rental.schemas import RentalResponseSchema
from sqlalchemy import select
from datetime import datetime

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

    @staticmethod
    def get_by_user(user_id):
        rentals = db.session.execute(select(Rental).filter_by(user_id=user_id)).scalars().all()
        return RentalResponseSchema(many=True).dump(rentals)

    @staticmethod
    def approve_rental(rental_id):
        rental = db.session.get(Rental, rental_id)
        if not rental:
            return False, "Rental not found"
        if rental.status != "PENDING":
            return False, "Only PENDING rentals can be approved"
        
        rental.status = "APPROVED"
        db.session.commit()
        return True, RentalResponseSchema().dump(rental)

    @staticmethod
    def reject_rental(rental_id):
        rental = db.session.get(Rental, rental_id)
        if not rental:
            return False, "Rental not found"
        if rental.status != "PENDING":
            return False, "Only PENDING rentals can be rejected"
        
        rental.status = "REJECTED"
        rental.car.is_available = True
        db.session.commit()
        return True, RentalResponseSchema().dump(rental)

    @staticmethod
    def start_rental(rental_id):
        rental = db.session.get(Rental, rental_id)
        if not rental:
            return False, "Rental not found"
        if rental.status != "APPROVED":
            return False, "Only APPROVED rentals can be started"
        
        rental.status = "ACTIVE"
        rental.start_time = datetime.utcnow()
        db.session.commit()
        return True, RentalResponseSchema().dump(rental)

    @staticmethod
    def close_rental(rental_id):
        rental = db.session.get(Rental, rental_id)
        
        if not rental:
            return False, "Rental not found"
        
        if rental.status != "ACTIVE":
            return False, "Only ACTIVE rentals can be closed"
            
        rental.status = "CLOSED"
        rental.car.is_available = True
        
        delta = rental.end_time - rental.start_time
        days = delta.days if delta.days > 0 else 1
            
        total_amount = days * rental.car.daily_price
        
        if not rental.invoice:
            invoice = Invoice(
                rental_id=rental.id,
                amount=total_amount,
                issued_at=datetime.utcnow(),
                paid=False
            )
            db.session.add(invoice)
            
        db.session.commit()
        
        return True, {
            "message": "Rental closed successfully",
            "rental_id": rental.id,
            "total_amount": total_amount
        }

    @staticmethod
    def get_invoice(rental_id):
        rental = db.session.get(Rental, rental_id)
        if not rental or not rental.invoice:
            return False, "Invoice not found for this rental"
        
        invoice = rental.invoice
        return True, {
            "id": invoice.id,
            "amount": invoice.amount,
            "issued_at": invoice.issued_at.isoformat(),
            "paid": invoice.paid
        }
