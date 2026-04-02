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
    if data is None:
        abort(400, description="Invalid JSON body")

    required_fields = ["url", "title"]
    for field in required_fields:
        if field not in data:
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

    query = Resource.query.filter_by(user_id=user_id)

    page = request.args.get("page", 1)
    limit = request.args.get("limit", 5)

    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        abort(400, description="page and limit must be integers")
    
    pagination = query.paginate(
        page = page,
        per_page = limit,
        error_out = False
    )

    resources = pagination.items

    return jsonify({
        "meta" : {
            "total": pagination.total,
            "page": page,
            "limit": limit,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        },
        "data": [resource.to_dict() for resource in resources]
    })

@resources_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_resource_by_id(id):
    user_id = int(get_jwt_identity())
    
    resource = Resource.query.get(id)
    if not resource:
        abort(404, description="Resource does not exist")
    
    if resource.user_id != user_id:
        abort(403, description="Resource does not belong to user")

    return resource.to_dict()

@resources_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_resource_by_id(id):
    user_id = int(get_jwt_identity())

    resource = Resource.query.get(id)

    if not resource:
        abort(404, description="Resource does not exist")

    if resource.user_id != user_id:
        abort(403, description="Resource does not belong to user")

    db.session.delete(resource)
    db.session.commit()

    return jsonify({
        "message": "Resource deleted successfully"
    }), 200
    
@resources_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_resource_by_id(id):
    user_id = int(get_jwt_identity())

    resource = Resource.query.get(id)

    if not resource:
        abort(404, description="Resource does not exist")

    if resource.user_id != user_id:
        abort(403, description="Resource does not belong to user")

    data = request.get_json()
    if data is None:
        abort(400, description="Invalid JSON body")

    if "title" in data:
        resource.title = data["title"]
    if "url" in data:
        resource.url = data["url"]
    if "description" in data:
        resource.description = data["description"]   

    db.session.commit() 
    return jsonify(resource.to_dict()), 200                    