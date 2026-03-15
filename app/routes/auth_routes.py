from flask import Blueprint, request, jsonify, abort 
from app.models.user import User
from app.extensions import db, bcrypt, jwt 
from flask_jwt_extended import create_access_token
from sqlalchemy import or_

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods = ["POST"])
def create_user():
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON body")

    required_fields = ["username", "email", "password"]

    for field in required_fields:
        if field not in data:
            abort(400, description=f"{field} is required")

    existing_user = User.query.filter_by(username=data["username"]).first()
    existing_email = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        abort(409, description="Username already exists")
    if existing_email:
        abort(409, description="Email already exists")
    try:
        user = User(
            username = data["username"],
            email = data["email"]
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods = ["POST"])
def user_login():
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON body")
    
    required_fields = ["identifier", "password"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"{field} is required")

    identifier = data["identifier"]
    password = data["password"]
    user = User.query.filter(
        or_(
            User.username == identifier,
            User.email == identifier
        )
    ).first()

    if not user or not user.check_password(password):
        abort(401, description="Invalid credentials")
    
    access_token = create_access_token(identity=user.id)

    return jsonify({
        "access_token": access_token,
        "user_id": user.id,
        "username": user.username
    }), 200

    


            
    

