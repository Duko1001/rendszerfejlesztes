from __future__ import annotations
from app import db, create_app
from config import Config
from datetime import datetime

app = create_app(config_class=Config)
from app import models
app.app_context().push()

print(app.config["SQLALCHEMY_DATABASE_URI"])

#User
from app.models.user import User
from app.models.role import Role

admin_role = Role(name="ADMIN")
user_role = Role(name="USER")
staff_role = Role(name="STAFF")

db.session.add_all([admin_role, user_role, staff_role])
db.session.commit()

admin = User(full_name="Admin User", email="admin@berauto.hu", password_hash="hashed_pw")
customer = User(full_name="Test Customer", email="customer@berauto.hu", password_hash="hashed_pw")
staff = User(full_name="Ugyintezo Bela", email="staff@berauto.hu", password_hash="hashed_pw")

db.session.add_all([admin, customer, staff])
db.session.commit()

admin.roles.append(admin_role)
customer.roles.append(user_role)
staff.roles.append(staff_role)

db.session.commit()

#Car
from app.models.car import Car

car1 = Car(brand="BMW", model="320d", year=2022, license_plate="ABC-123", daily_price=20000, mileage=50000)
car2 = Car(brand="Audi", model="A4", year=2021, license_plate="DEF-456", daily_price=18000, mileage=60000)

db.session.add_all([car1, car2])
db.session.commit()

#Test User+Car
print("\nUser lista:")
for u in User.query.all():
    print(u.id, u.full_name, [r.name for r in u.roles])

print("\nCar lista:")
for c in Car.query.all():
    print(c.id, c.brand, c.model, c.license_plate)

#Rental
from app.models.rental import Rental

rental1 = Rental(user=db.session.get(User, 2), car=db.session.get(Car, 1), start_time=datetime(2026, 3, 10, 10, 0), end_time=datetime(2026, 3, 10, 14, 0), status="APPROVED")

db.session.add(rental1)
db.session.commit()

#Invoice
from app.models.invoice import Invoice

invoice1 = Invoice(rental=db.session.get(Rental, 1), amount=100000)

db.session.add(invoice1)
db.session.commit()

#Test Rental+Invoice
print("\nRental lista:")
for r in Rental.query.all():
    print(r.id, r.user.full_name, r.car.model, r.status)

print("\nInvoice lista:")
for i in Invoice.query.all():
    print(i.id, i.amount, i.rental.car.model)