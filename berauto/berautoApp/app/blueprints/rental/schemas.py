from marshmallow import Schema, fields


class RentalCreateSchema(Schema):
    user_id = fields.Integer(required=True)
    car_id = fields.Integer(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)


class RentalResponseSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    car_id = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.String()
    created_at = fields.DateTime()


class CloseRentalResponseSchema(Schema):
    message = fields.String()
    rental_id = fields.Integer()
    total_amount = fields.Float()