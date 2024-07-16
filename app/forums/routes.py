from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import ForumPost
from app.extensions import db
from .schemas import forum_post_schema, forum_posts_schema

forums_bp = Blueprint('forums', __name__)

@forums_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.form    
    new_post = ForumPost(
        course_id=data['course_id'],
        user_id=data['user_id'],
        content=data['content']
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify(forum_post_schema.dump(new_post)), 201

@forums_bp.route('/<int:course_id>', methods=['GET'])
def get_posts(course_id):
    posts = ForumPost.query.filter_by(course_id=course_id).all()
    return jsonify(forum_posts_schema.dump(posts)), 200

@forums_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    return jsonify(forum_post_schema.dump(post)), 200

@forums_bp.route('/post/<int:post_id>', methods=['PUT','PATCH'])
@jwt_required()
def update_post(post_id):
    data = request.form
    post = ForumPost.query.get_or_404(post_id)
    if 'content' in data:
        post.content = data['content']
    db.session.commit()
    return jsonify(forum_post_schema.dump(post)), 200

@forums_bp.route('/post/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Post deleted successfully"}), 200
