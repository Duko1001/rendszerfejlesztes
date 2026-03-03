from app.extensions import db


class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)

    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    daily_price = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Integer, default=0)
    is_available = db.Column(db.Boolean, default=True)
    rentals = db.relationship("Rental", back_populates="car")
