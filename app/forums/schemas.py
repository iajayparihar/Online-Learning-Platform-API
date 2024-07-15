from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import ForumPost
from app.extensions import db

class ForumPostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ForumPost
        sqla_session = db.session


class ForumPostCreateSchema(Schema):
    course_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    content = fields.Str(required=True)
