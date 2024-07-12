from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import ForumPost
from app.extensions import db

forums_bp = Blueprint('forums', __name__)

@forums_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    new_post = ForumPost(
        course_id=data['course_id'],
        user_id=data['user_id'],
        content=data['content']
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"msg": "Post created successfully"}), 201

@forums_bp.route('/<int:course_id>', methods=['GET'])
def get_posts(course_id):
    posts = ForumPost.query.filter_by(course_id=course_id).all()
    return jsonify([post.content for post in posts]), 200
