from marshmallow import Schema, fields

class PurchaseSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    date = fields.DateTime(dump_only=True)
