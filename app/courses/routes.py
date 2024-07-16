from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Course
from app.extensions import db
from .schemas import course_schema, courses_schema

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    data = request.form
    new_course = Course(title=data['title'], description=data.get('description'))
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"msg": "Course created successfully"}), 201

@courses_bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify(courses_schema.dump(courses)), 200


@courses_bp.route('/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def update_course(id):
    data = request.form
    course = Course.query.get_or_404(id)
    course.title = data.get('title', course.title)
    course.description = data.get('description', course.description)
    db.session.commit()
    return jsonify({"msg": "Course updated successfully","course": course_schema.dump(course)}), 200

@courses_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"msg": "Course deleted successfully"}), 200

