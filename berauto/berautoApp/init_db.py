from __future__ import annotations
from app import db, create_app
from config import Config
from datetime import date

app = create_app(config_class=Config)
from app import models
app.app_context().push()

print(app.config["SQLALCHEMY_DATABASE_URI"])

#User
from app.models.user import User, UserRole
admin = User(full_name="Admin User", email="admin@berauto.hu", password_hash="hashed_pw", role=UserRole.ADMIN)
customer = User(full_name="Test Customer", email="customer@berauto.hu", password_hash="hashed_pw", role=UserRole.USER)
staff = User(full_name="Ugyintezo Bela", email="staff@berauto.hu", password_hash="hashed_pw", role=UserRole.STAFF)
db.session.add_all([admin, customer, staff])
db.session.commit()

#Car
from app.models.car import Car
car1 = Car(brand="BMW", model="320d", year=2022, license_plate="ABC-123", daily_price=20000, is_available=True, mileage=50000)
car2 = Car(brand="Audi", model="A4", year=2021, license_plate="DEF-456", daily_price=18000, is_available=True, mileage=60000)
db.session.add_all([car1, car2])
db.session.commit()

#Test User+Car
print("\nUser lista:")
for u in User.query.all():
    print(u.id, u.full_name, u.role.name)

print("\nCar lista:")
for c in Car.query.all():
    print(c.id, c.brand, c.model, c.license_plate)