from marshmallow import Schema, fields

class ContactSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    message = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

class ContactCreateSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    message = fields.Str(required=True)
