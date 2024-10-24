#!/usr/bin/env python3
'''create a flask App'''

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_route():
    '''create a flask app with a get route'''
    return jsonify(message="Bienvenue")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
