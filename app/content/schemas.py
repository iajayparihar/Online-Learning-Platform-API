from marshmallow import Schema, fields, validate

class ContentSchema(Schema):
    id = fields.Int(dump_only=True)
    course_id = fields.Int(required=True)
    content_type = fields.Str(required=True, validate=validate.Length(min=1))
    content_url = fields.Str(validate=validate.URL())
    text_content = fields.Str()

content_schema = ContentSchema()
contents_schema = ContentSchema(many=True)
