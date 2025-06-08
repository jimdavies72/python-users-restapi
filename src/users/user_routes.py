
from flask import Blueprint, request, jsonify, current_app
from users.user_model import UserModel
from pydantic import ValidationError
from bson import ObjectId

import requests

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

@users_blueprint.route('/<email>', methods=['PUT'])
def update_user(email):
    data = request.get_json()
    db = current_app.config["db"]
    result = db["users"].update_one({"email": email}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "User updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@users_blueprint.route('/<email>', methods=['DELETE'])
def delete_user(email):
    db = current_app.config["db"]
    result = db["users"].delete_one({"email": email})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@users_blueprint.route('/delete_all', methods=['DELETE'])
def delete_all_user():
    # WARNING: DELETES ALL USERS
  
    db = current_app.config["db"]
    result = db["users"].delete_many({})
    if result.deleted_count > 0:
        return jsonify({"message": "Users deleted successfully"}), 200
    return jsonify({"error": "Users not found"}), 404
  
@users_blueprint.route('/from_api', methods=['POST'])
def create_user_from_api():
    try:
      # extract [get] data from 3rd party api
      response = requests.get('https://jsonplaceholder.typicode.com/users')
      response.raise_for_status() # raise exception if request failure
      data = response.json()
      
      # transform response to correct data schema
      transformed = [
        {
          "name": user["name"],
          "email": user["email"],
          "password": user["username"]
        }
        for user in data
      ]
      
      # load data into db
      collection = current_app.config["db"]["users"]
      collection.insert_many(transformed)
      return jsonify({
        "message": "Users created successfully",
        "count": len(transformed)
      }), 201
      
    except requests.RequestException as e:
      return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 404
    except Exception as e:
      return jsonify({"error": f"Something went wrong: {str(e)}"}), 500