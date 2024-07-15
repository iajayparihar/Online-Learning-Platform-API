from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import ForumPost
from app.extensions import db
from .schemas import ForumPostSchema, ForumPostCreateSchema

forums_bp = Blueprint('forums', __name__)

forum_post_schema = ForumPostSchema()
forum_posts_schema = ForumPostSchema(many=True)
forum_post_create_schema = ForumPostCreateSchema()

@forums_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    errors = forum_post_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    new_post = ForumPost(
        course_id=data['course_id'],
        user_id=data['user_id'],
        content=data['content']
    )
    db.session.add(new_post)
    db.session.commit()
    return forum_post_schema.jsonify(new_post), 201

@forums_bp.route('/<int:course_id>', methods=['GET'])
def get_posts(course_id):
    posts = ForumPost.query.filter_by(course_id=course_id).all()
    return forum_posts_schema.jsonify(posts), 200

@forums_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    return forum_post_schema.jsonify(post), 200

@forums_bp.route('/post/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    data = request.get_json()
    errors = forum_post_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    post = ForumPost.query.get_or_404(post_id)
    if 'content' in data:
        post.content = data['content']
    db.session.commit()
    return forum_post_schema.jsonify(post), 200

@forums_bp.route('/post/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Post deleted successfully"}), 200
