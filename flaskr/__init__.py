import os
import json
from functools import wraps
from flask import Flask, jsonify, request, abort

def as_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return jsonify(
                f(json.loads(request.data), *args, **kwargs)
            )
        except Exception as e:
            abort(400)
    return wrapper

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    @app.route('/', methods=(['GET']))
    def welcome():
        return b"Hello world!"

    @app.route('/digits/sum', methods=(['POST']))
    @as_json
    def digits_sum(data):
        values_sum = sum(data["address"]["values"])
        digits_iter = map(int, str(values_sum))
        result = sum(digits_iter)
        return {"result": result}

    return app
