from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Content
from app.extensions import db
from .schemas import content_schema, contents_schema

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
    return jsonify({"msg": "Content added successfully", "content": content_schema.dump(new_content)}), 201

@content_bp.route('/course/<int:course_id>', methods=['GET'])
def get_content_by_course(course_id):   
    contents = Content.query.filter_by(course_id=course_id).all()
    return jsonify(contents_schema.dump(contents)), 200


@content_bp.route('/<int:content_id>', methods=['GET'])
def get_content_detail(content_id):
    content = Content.query.get_or_404(content_id)
    return jsonify(content_schema.dump(content)), 200


@content_bp.route('/<int:content_id>', methods=['PUT','PATCH'])
@jwt_required()
def update_content(content_id):
    content = Content.query.get_or_404(content_id)
    data = request.form
    content.content_type = data.get('content_type',content.content_type)
    content.content_url = data.get('content_url', content.content_url)
    content.text_content = data.get('text_content', content.text_content)
    db.session.commit()
    return jsonify({"msg": "Content updated successfully", "content" : content_schema.dump(content)}), 200

@content_bp.route('/<int:content_id>', methods=['DELETE'])
@jwt_required()
def delete_content(content_id):
    content = Content.query.get_or_404(content_id)
    db.session.delete(content)
    db.session.commit()
    return jsonify({"msg": "Content deleted successfully"}), 200

@content_bp.route('/allContent', methods=['GET'])
def get_all_content():
    all_content = Content.query.all()
    return jsonify(contents_schema.dump(all_content)), 200