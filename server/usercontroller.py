from flask import Flask, jsonify, request, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from bson.json_util import dumps, loads

from mongoDB import db


def signupC(bcrypter):
    user = request.json
    pw_hash = bcrypter.generate_password_hash(user['password'])  ## from flask_bcrypt import Bcrypt
    user['password'] = pw_hash.decode("utf-8")
    _id = db.users.insert(user)
    _id = str(_id)
    return jsonify({"_id": _id})


def loginC(bcrypter):
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

    if email != found['email'] or not bcrypter.check_password_hash(found['password'], password):
        return jsonify({"msg": "Bad email or password"}), 401

    # Identity can be any data that is json serializable
    # https://flask-jwt-extended.readthedocs.io/en/latest/blacklist_and_token_revoking.html#blacklist-and-token-revoking
    ret = {
        'access_token': create_access_token(identity=email),
        'refresh_token': create_refresh_token(identity=email)
    }
    return jsonify(ret), 200
    



def protectedC():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def getUsersC():
    mongoColl = db.users.find()
    return Response(dumps(mongoColl), mimetype="application/json")
