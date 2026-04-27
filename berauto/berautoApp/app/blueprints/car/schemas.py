from marshmallow import Schema, fields

class CarRequestSchema(Schema):
    brand = fields.String(required=True)
    model = fields.String(required=True)
    year = fields.Integer(required=True)
    license_plate = fields.String(required=True)
    daily_price = fields.Float(required=True)
    mileage = fields.Integer()

class CarResponseSchema(Schema):
    id = fields.Integer()
    brand = fields.String()
    model = fields.String()
    year = fields.Integer()
    license_plate = fields.String()
    daily_price = fields.Float()
    mileage = fields.Integer()