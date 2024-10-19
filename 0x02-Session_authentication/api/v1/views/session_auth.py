#!/usr/bin/env python3
""" Module of session authentication views
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
import os
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    '''route for authenticating entered login details'''
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:  # if no user found
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):  # if password is not valid/same
        return jsonify({"error": "wrong password"}), 401

    '''create a session id for user id'''
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = make_response(user.to_json())
    # return dict representation of user
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    # use value of the env var as cookie name

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    '''logout from the session'''
    from api.v1.app import auth
    deleted_session = auth.destroy_session(request)
    if not deleted_session:
        abort(404)
    return jsonify({}), 200
