from app.extensions import db
from app.models.car import Car
from sqlalchemy import select

class CarService:

    @staticmethod
    def get_all():
        cars = db.session.execute(select(Car)).scalars().all()
        return True, cars

    @staticmethod
    def get_one(cid):
        car = db.session.get(Car, cid)
        if not car:
            return False, "Car not found"
        return True, car

    @staticmethod
    def add(data):
        try:
            car = Car(
                brand=data["brand"],
                model=data["model"],
                year=data["year"],
                license_plate=data["license_plate"],
                daily_price=data["daily_price"],
                mileage=data.get("mileage", 0)
            )
            db.session.add(car)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False, str(e)

        return True, car

    @staticmethod
    def update(cid, data):
        try:
            car = db.session.get(Car, cid)
            if not car:
                return False, "Car not found"

            car.brand = data.get("brand", car.brand)
            car.model = data.get("model", car.model)
            car.daily_price = data.get("daily_price", car.daily_price)
            car.year = data.get("year", car.year)
            car.license_plate = data.get("license_plate", car.license_plate)
            car.mileage = data.get("mileage", car.mileage)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False, str(e)

        return True, car

    @staticmethod
    def delete(cid):
        try:
            car = db.session.get(Car, cid)
            if not car:
                return False, "Car not found"

            db.session.delete(car)
            db.session.commit()
        except Exception as e:
            return False, str(e)

        return True, "Deleted"