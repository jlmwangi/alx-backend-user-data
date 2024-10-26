#!/usr/bin/env python3
'''create a flask App'''

from flask import Flask, jsonify, request, abort, make_response, url_for
from flask import redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

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


@app.route('/sessions', methods=['POST'])
def login():
    '''confirm login information'''
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        sess_id = AUTH.create_session(email)
        resp = make_response(jsonify(email=email, message="logged in"))
        resp.set_cookie("session_id", sess_id)
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    '''logout by destroying a session'''
    session_id = request.cookies.get('session_id')
    #  find user with requested sesh id
    try:
        user_from_sessionid = AUTH.get_user_from_session_id(session_id)
        if user_from_sessionid:
            AUTH.destroy_session(user_from_sessionid.id)
            return redirect(url_for('get_route'))
        abort(403)
    except NoResultFound:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    '''confirm user profile'''
    session_id = request.cookies.get('session_id')

    try:
        user_sessionid = AUTH.get_user_from_session_id(session_id)
        if user_sessionid:
            return jsonify(email=user_sessionid.email), 200
        abort(403)
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    '''responds to post request to reset password'''
    email = request.form.get('email')
    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify(email=email, reset_token=reset_token), 200
    except NoResultFound:
        abort(403)

@app.route('/reset_password', methods=['PUT'])
def update_password():
    '''updates the password'''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        updated_password = AUTH.update_password(reset_token, new_password)
        return jsonify(email=email, message="Password updated"), 200
    except Exception:
        aboth(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
