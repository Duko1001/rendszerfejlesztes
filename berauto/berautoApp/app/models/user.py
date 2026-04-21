from app.models.role import Role
from app.models.association import user_roles
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    full_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(50))

    roles = db.relationship("Role", secondary=user_roles, backref="users")
    is_active = db.Column(db.Boolean, default=True)

    rentals = db.relationship("Rental", back_populates="user", cascade="all, delete")