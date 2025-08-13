from marshmallow import Schema, fields

class LoginSchema(Schema):
    username = fields.Str(required=True, metadata={"description": "Admin username"})
    password = fields.Str(required=True, load_only=True, metadata={"description": "Admin password"})

class RegisterSchema(Schema):
    username = fields.Str(required=True, metadata={"description": "Desired admin username"})
    password = fields.Str(required=True, load_only=True, metadata={"description": "Desired admin password"})

class TokenSchema(Schema):
    access_token = fields.Str(required=True, dump_only=True, metadata={"description": "JWT access token"})
    token_type = fields.Str(required=True, dump_only=True, metadata={"description": "Token type"}, default="bearer")
