from flask import Flask, jsonify, request, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt
import logging


#eigene
import control.usercontroller as usercontroller
import control.filecontroller as filecontroller
import app_settings

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = app_settings.jwtSecret  # Change this!
app.debug=True
app_bcrypt = Bcrypt(app)
# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)
logging.basicConfig(filename=app_settings.logfile ,level=logging.INFO)

logging.info('START APP')


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    return usercontroller.login(app_bcrypt)


@app.route('/signup', methods=['POST'])
def signup():
    return usercontroller.signup(app_bcrypt)


@app.route('/users', methods=['GET'])
def getUsers():
    return usercontroller.getUsers()


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return usercontroller.protected()


@jwt_required
@app.route('/uploader', methods = ['POST'])
def uploader():
    return filecontroller.upload_file()


if __name__ == '__main__':
    app.run()
