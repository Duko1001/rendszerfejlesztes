from app.extensions import db
from app.models.user import User
from app.models.role import Role
from app.blueprints.user.schemas import UserResponseSchema
from sqlalchemy import select

class UserService:

    @staticmethod
    def register(data):
        if db.session.execute(select(User).filter_by(email=data["email"])).scalar_one_or_none():
            return False, "Email already exists"

        user = User(full_name=data["full_name"], email=data["email"], password_hash=data["password"])

        role = db.session.execute(select(Role).filter_by(name="USER")).scalar_one()
        user.roles.append(role)

        db.session.add(user)
        db.session.commit()

        return True, UserResponseSchema().dump(user)

    @staticmethod
    def login(data):
        user = db.session.execute(select(User).filter_by(email=data["email"])).scalar_one_or_none()

        if not user or user.password_hash != data["password"]:
            return False, "Invalid login"

        return True, UserResponseSchema().dump(user)

    @staticmethod
    def add_role_to_user(json_data):
        try:
            user = db.session.get(User, json_data["user_id"])
            role = db.session.get(Role, json_data["role_id"])

            if not user or not role:
                return False, "User or Role not found"

            user.roles.append(role)
            db.session.commit()
        except:
            return False, "Role assign error"

        return True, user

    @staticmethod
    def list_roles():
        roles = db.session.query(Role).all()
        return True, roles

    @staticmethod
    def get_user_roles(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return False, "User not found"
        return True, user.roles

    @staticmethod
    def delete(user_id):
        try:
            user = db.session.get(User, user_id)
            if not user:
                return False, "User not found"

            db.session.delete(user)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return False, str(e)

        return True, "User deleted"