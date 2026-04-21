from app.extensions import db
from sqlalchemy import Enum
import enum
from datetime import datetime


class RentalStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(Enum(RentalStatus), nullable=False, default=RentalStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    user = db.relationship("User", back_populates="rentals")
    car = db.relationship("Car", back_populates="rentals")
    invoice = db.relationship("Invoice", back_populates="rental", uselist=False, cascade="all, delete-orphan")