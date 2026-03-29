from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.resource import Resource
from app.models.user import User
from app.extensions import db

resources_bp = Blueprint("resources", __name__)

@resources_bp.route("", methods=["POST"])
@jwt_required()
def create_resource():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON body")

    required_fields = ["url", "title"]
    for field in required_fields:
        if not field:
            abort(400, description=f"{field} is required")

    title = data["title"]
    url = data["url"]
    description = data["description"]
    
    resource =Resource(
        user_id = user_id,
        title = title,
        url = url,
        description = description
    )

    db.session.add(resource)
    db.session.commit()

    return jsonify({
        "message": "Resource created",
        "id": resource.id
    }), 201

@resources_bp.route("", methods=["GET"])
@jwt_required()
def get_resources():
    user_id = int(get_jwt_identity())

    resources = Resource.query.filter_by(user_id=user_id).all()

    return [resource.to_dict() for resource in resources]

@resources_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_resource_by_id(id):
    user_id = int(get_jwt_identity())
    
    resource = Resource.query.get(id)
    if not resource:
        abort(404, description="Resource does not exist")
    
    if resource.user_id == user_id:
        return resource.to_dict()
    else:
        abort(403, description="Resource does not belong to user")


@resources_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_resource_by_id(id):
    user_id = int(get_jwt_identity())

    resource = Resource.query.get(id)

    if not resource:
        abort(404, description="Resource does not exist")

    if resource.user_id == user_id:
        db.session.delete(resource)
        db.session.commit()

        return jsonify({
            "message": "Resource deleted successfully"
        }), 200
    else:
        abort(403, description="Resource does not belong to user")
    
