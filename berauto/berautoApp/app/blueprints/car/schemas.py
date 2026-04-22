from marshmallow import Schema, fields

class CarRequestSchema(Schema):
    brand = fields.String()
    model = fields.String()
    daily_price = fields.Float()

class CarResponseSchema(Schema):
    id = fields.Integer()
    brand = fields.String()
    model = fields.String()
    daily_price = fields.Float()