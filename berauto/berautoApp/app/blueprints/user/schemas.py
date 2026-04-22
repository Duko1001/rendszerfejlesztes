from marshmallow import Schema, fields
from apiflask.fields import String
from apiflask.validators import Email

class UserRequestSchema(Schema):
    full_name = fields.String(required=True)
    email = String(required=True, validate=Email())
    password = fields.String(required=True)

class UserResponseSchema(Schema):
    id = fields.Integer()
    full_name = fields.String()
    email = fields.String()

class UserLoginSchema(Schema):
    email = String(required=True, validate=Email())
    password = fields.String(required=True)

class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()

class UserRoleAssignSchema(Schema):
    user_id = fields.Integer()
    role_id = fields.Integer()