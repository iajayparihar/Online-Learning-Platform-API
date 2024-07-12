from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Content
from app.extensions import db

content_bp = Blueprint('content', __name__)

@content_bp.route('/', methods=['POST'])
@jwt_required()
def add_content():
    data = request.form
    new_content = Content(
        course_id=data['course_id'],
        content_type=data['content_type'],
        content_url=data.get('content_url'),
        text_content=data.get('text_content')
    )
    db.session.add(new_content)
    db.session.commit()
    return jsonify({"msg": "Content added successfully"}), 201

@content_bp.route('/<int:course_id>', methods=['GET'])
def get_content(course_id):
    contents = Content.query.filter_by(course_id=course_id).all()
    return jsonify([content.content_type for content in contents]), 200
