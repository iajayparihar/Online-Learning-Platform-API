from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token
from app.models import User
from app.extensions import db, jwt
from .schemas import users_schema, user_schema
import logging
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

from app import create_app

auth_bp = Blueprint('auth', __name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Create a Limiter object
# limiter = Limiter(
#     get_remote_address,
#     app=create_app(),
#     default_limits=["200 per day", "50 per hour"]
# )

@auth_bp.route('/register', methods=['POST'])
# @limiter.limit("10 per minute")  # This route is limited to 10 requests per minute
def register():
    logger.debug("Register endpoint called")
    data = request.form

    name = data['name']
    username = data['username']
    password1 = data['password1']
    password2 = data['password2']
    email = data['email']
    mobile = data['mobile']
    address = data['address']
    logger.debug(f"Data received: {data}")

    if password1 != password2:
        logger.error("Passwords do not match")
        return jsonify({'message': 'User Password is not Same'}), 400
    user = User(username=username, password=generate_password_hash(password1), name=name, email=email, mobile=mobile, address = address)
    user_data = user_schema.dump(user)

    try:
        db.session.add(user)
        db.session.commit()
        logger.debug("User added to database")
    except Exception as e:
        logger.error(f"Error adding user to database: {e}")
        db.session.rollback()
        return jsonify({'message': 'Error registering user'}), 500

    return jsonify({'message': 'User registered successfully', "user": user_data}), 201


@auth_bp.route('/login', methods=['POST'])
# @limiter.limit("5 per minute")  # This route is limited to 5 requests per minute
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    if not user: 
        return jsonify({'message': 'User not found'}), 404

    if user and check_password_hash(user.password,password):
        access_token = create_access_token(identity=user.id)
        ref = create_refresh_token(identity=user.id)    

        return jsonify({'user' : user_schema.dump(user), 'Access Token': access_token, 'Refresh Token' : ref}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


@auth_bp.route('/allusers',methods=['GET'])
@jwt_required()
def getting_all_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200


@auth_bp.route('/update/<int:id>',methods=['PUT','PATCH'])
@jwt_required()
def user_update(id):
    with current_app.app_context():
        user = db.session.get(User, id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

    data = request.form
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.mobile = data.get('mobile', user.mobile)
    user.password = data.get('password', user.password)
    user.address = data.get('address', user.address )

    db.session.commit()

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "mobile": user.mobile,
        "address" : user.address,
    })


@auth_bp.route('/delete/<int:id>',methods=['delete'])
@jwt_required()
def user_delete_model(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return f'user {id=} is deleted'