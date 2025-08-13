from marshmallow import Schema, fields

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), required=False)
    is_featured = fields.Bool(required=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ProjectCreateSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), required=False)
    is_featured = fields.Bool(required=False)

class ProjectUpdateSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    url = fields.Str()
    tags = fields.List(fields.Str())
    is_featured = fields.Bool()
