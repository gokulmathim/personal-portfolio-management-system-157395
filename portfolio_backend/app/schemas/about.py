from marshmallow import Schema, fields

class AboutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(allow_none=True)
    title = fields.Str(allow_none=True)
    bio = fields.Str(allow_none=True)
    email = fields.Email(allow_none=True)
    location = fields.Str(allow_none=True)
    avatar_url = fields.Str(allow_none=True)
    social_links = fields.Dict(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class AboutUpdateSchema(Schema):
    name = fields.Str()
    title = fields.Str()
    bio = fields.Str()
    email = fields.Email()
    location = fields.Str()
    avatar_url = fields.Str()
    social_links = fields.Dict()
