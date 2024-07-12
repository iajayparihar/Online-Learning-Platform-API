from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    mobile = fields.Str(required=True)
    address = fields.Str(required=True)
    # password = fields.Str(required=True)

users_schema = UserSchema(many=True)
user_schema = UserSchema()