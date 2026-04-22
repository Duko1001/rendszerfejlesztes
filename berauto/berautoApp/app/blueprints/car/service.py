from app.extensions import db
from app.models.car import Car
from sqlalchemy import select

class CarService:

    @staticmethod
    def get_all():
        cars = db.session.execute(select(Car)).scalars()
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
            car = Car(**data)
            db.session.add(car)
            db.session.commit()
        except:
            return False, "Car add error"
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

            db.session.commit()
        except:
            return False, "Car update error"

        return True, car

    @staticmethod
    def delete(cid):
        try:
            car = db.session.get(Car, cid)
            if not car:
                return False, "Car not found"

            db.session.delete(car)
            db.session.commit()
        except:
            return False, "Car delete error"

        return True, "Deleted"