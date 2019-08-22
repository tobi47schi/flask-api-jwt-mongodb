from flask import Flask, jsonify, request, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt
from bson.json_util import dumps, loads
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
with client:
    db = client.testdb

#db.users.drop()
db.users.create_index("username", unique=True)



app = Flask(__name__)
bcrypt = Bcrypt(app)
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    
    found = db.users.find_one({"username" : username})
    if not found : 
        return jsonify({"msg": "User not found"}), 400

    if username != found['username'] or not bcrypt.check_password_hash(found['password'], password):
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route('/signup', methods=['POST'])

def signup():
    user = request.json
    pw_hash = bcrypt.generate_password_hash(user['password']) ## from flask_bcrypt import Bcrypt
    user['password'] = pw_hash.decode("utf-8")
    _id = db.users.insert(user)
    _id = str(_id)
    return jsonify({"_id" : _id})


@app.route('/users', methods=['GET'])
def getUsers():
    mongoColl = db.users.find()
    return Response(dumps(mongoColl) , mimetype = "application/json")


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200





if __name__ == '__main__':
    app.run()