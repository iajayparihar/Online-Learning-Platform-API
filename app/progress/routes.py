from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Progress
from app.extensions import db

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/', methods=['POST'])
@jwt_required()
def update_progress():
    data = request.get_json()
    progress = Progress.query.filter_by(user_id=data['user_id'], course_id=data['course_id']).first()
    if progress:
        progress.progress_percentage = data['progress_percentage']
    else:
        new_progress = Progress(
            user_id=data['user_id'],
            course_id=data['course_id'],
            progress_percentage=data['progress_percentage']
        )
        db.session.add(new_progress)
    db.session.commit()
    return jsonify({"msg": "Progress updated successfully"}), 200

@progress_bp.route('/<int:user_id>/<int:course_id>', methods=['GET'])
@jwt_required()
def get_progress(user_id, course_id):
    progress = Progress.query.filter_by(user_id=user_id, course_id=course_id).first()
    if progress:
        return jsonify({"progress_percentage": progress.progress_percentage}), 200
    return jsonify({"msg": "No progress found"}), 404
