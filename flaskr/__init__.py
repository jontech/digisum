import os
from functools import wraps
from flask import Flask, jsonify, request, abort

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    @app.route('/', methods=(['GET']))
    def welcome():
        return b"Hello world!"

    @app.route('/digits/sum', methods=(['POST']))
    def digits_sum():
        values_sum = sum(request.json["address"]["values"])
        digits_iter = map(int, str(values_sum))
        result = sum(digits_iter)
        return jsonify({"result": result})

    return app
