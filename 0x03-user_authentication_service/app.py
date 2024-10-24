#!/usr/bin/env python3
'''create a flask App'''

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'])
def get_route():
    '''create a flask app with a get route'''
    return jsonify(message="Bienvenue")


@app.route('/users', methods=['POST'])
def users():
    '''implement an endpoint to register a user'''
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        registered_user = AUTH.register_user(email, password)
        if registered_user:  # if registering was successful
            return jsonify(email=email, message="user created")
    except ValueError:
        return jsonify(message="email already registered"), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
