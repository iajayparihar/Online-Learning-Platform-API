from marshmallow import Schema, fields

class ForumPostCreateSchema(Schema):
    course_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    content = fields.Str(required=True)

forum_post_schema = ForumPostCreateSchema()
forum_posts_schema = ForumPostCreateSchema(many=True)