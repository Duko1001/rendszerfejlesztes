from marshmallow import Schema, fields

class RentalCreateSchema(Schema):
    car_id = fields.Integer(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

class RentalResponseSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    car_id = fields.Integer()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    status = fields.String()
    created_at = fields.DateTime()