from flask import Flask, jsonify, request, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from bson.json_util import dumps, loads
from mongoDB import db


def signup(app_bcrypt):
    user = request.json
    #pw_hash = app_bcrypt.generate_password_hash(user['password'])  ## from flask_bcrypt import Bcrypt
    #user['password'] = pw_hash.decode("utf-8")
    _id = db.users.insert(user)
    _id = str(_id)
    return jsonify({"_id": _id})


def login(app_bcrypt):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    found = db.users.find_one({"email": email})
    if not found:
        return jsonify({"msg": "User not found"}), 400

    #if email != found['email'] or not app_bcrypt.check_password_hash(found['password'], password):
    #    return jsonify({"msg": "Bad email or password"}), 401
    if email != found['email'] or  found['password'] != password:
        return jsonify({"msg": "Bad email or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=dumps(found))
    return jsonify(access_token=access_token), 200


def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return Response(current_user, status=200, mimetype="application/json")

def getUsers():
    mongoColl = db.users.find()
    return Response(dumps(mongoColl), mimetype="application/json")