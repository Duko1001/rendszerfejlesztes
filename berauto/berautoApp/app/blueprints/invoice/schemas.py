from marshmallow import Schema, fields

class InvoiceResponseSchema(Schema):
    id = fields.Integer()
    rental_id = fields.Integer()
    amount = fields.Float()
    issued_at = fields.DateTime()
    paid = fields.Boolean()