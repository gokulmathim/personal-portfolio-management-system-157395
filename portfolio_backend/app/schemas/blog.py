from marshmallow import Schema, fields

class BlogSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    slug = fields.Str(required=True)
    content = fields.Str(required=True)
    is_published = fields.Bool(required=True)
    meta = fields.Dict(required=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class BlogCreateSchema(Schema):
    title = fields.Str(required=True)
    slug = fields.Str(required=True)
    content = fields.Str(required=True)
    is_published = fields.Bool(required=False)
    meta = fields.Dict(required=False)

class BlogUpdateSchema(Schema):
    title = fields.Str()
    slug = fields.Str()
    content = fields.Str()
    is_published = fields.Bool()
    meta = fields.Dict()
