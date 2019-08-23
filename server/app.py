from flask import Flask, jsonify, request, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt

#eigene
from control.usercontroller import signupC, loginC, protectedC, getUsersC

app = Flask(__name__)
app.debug=True
bcrypter = Bcrypt(app)
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    return loginC(bcrypter)


@app.route('/signup', methods=['POST'])
def signup():
    return signupC(bcrypter)


@app.route('/users', methods=['GET'])
def getUsers():
    return getUsersC()


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return protectedC()


if __name__ == '__main__':
    app.run()
