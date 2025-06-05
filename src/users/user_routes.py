
from flask import Blueprint, request, jsonify, current_app
from users.user_model import UserModel
from pydantic import ValidationError
from bson import ObjectId

users_blueprint = Blueprint('users_blueprint', __name__)

def serialize_user(user_doc):
    """Convert MongoDB document to JSON-serializable dict"""
    user_doc["id"] = str(user_doc["_id"])
    del user_doc["_id"]
    return user_doc

@users_blueprint.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        # Validate input data with Pydantic
        user = UserModel(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    #db = current_app.db
    db = current_app.config["db"]
    user_dict = user.model_dump(by_alias=True, exclude={"id"})
    # Insert user into MongoDB
    result = db["users"].insert_one(user_dict)
    return jsonify({"message": "User created successfully", "id": str(result.inserted_id)}), 201

@users_blueprint.route('/', methods=['GET'])
def get_users():
    #db = current_app.db
    db = current_app.config["db"]
    users_cursor = db["users"].find()
    users = [serialize_user(u) for u in users_cursor]
    return jsonify(users), 200

@users_blueprint.route('/<email>', methods=['GET'])
def get_user(email):
    db = current_app.config["db"]
    user = db["users"].find_one({"email": email})
    if user:
        return jsonify(serialize_user(user)), 200
    return jsonify({"error": "User not found"}), 404