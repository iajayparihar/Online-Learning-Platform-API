from marshmallow import Schema, fields, validate

class CourseSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(validate=validate.Length(max=500))

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
