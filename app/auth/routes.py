from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token
from app.models import User
from app.extensions import db, jwt
from .schemas import users_schema, user_schema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.form

    name = data['name']
    username = data['username']
    password1 = data['password1']
    password2 = data['password2']
    email = data['email']
    mobile = data['mobile']
    address = data['address']

    if password1 != password2:
        return jsonify({'message': 'User Password is not Same'}), 201  
    import pdb;pdb.set_trace()
    user = User(username=username, password=generate_password_hash(password1), name=name, email=email, mobile=mobile, address = address)
    user_data = user_schema.dump(user)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', "user" : user_data }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    # import pdb;pdb.set_trace()
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    if not user: 
        return jsonify({'message': 'User not found'}), 401

    if user and check_password_hash(user.password,password):
        access_token = create_access_token(identity=user.id)
        ref = create_refresh_token(identity=user.id)    

        return jsonify({'user' : user_schema.dump(user), 'Access Token': access_token, 'Refresh Token' : ref}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


@auth_bp.route('/allusers',methods=['GET'])
@jwt_required()
def getting_all_users():
        users = User.query.all()
        return jsonify(users_schema.dump(users))


@auth_bp.route('/update/<int:id>',methods=['PUT','PATCH'])
@jwt_required()
def user_patch_update(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

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