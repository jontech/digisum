import os
from functools import wraps
from flask import Flask, jsonify, request, abort

def validate_json(validators):
    def decorate(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if isinstance(request.json, dict):
                try:
                    result = map(lambda valid: valid(request.json or {}), validators)
                    errors = filter(lambda pair: pair[0], result)
                    if any(errors):
                        return jsonify({"errors": list(map(lambda pair: pair[1], errors))}), 400
                    else:
                        return f(*args, **kwargs)
                except KeyError as e:
                    return jsonify({"errors": ["Missing key {} in json object".format(e)]}), 400
            else:
                return jsonify({"errors": ["Malformed json"]}), 400
        return wrapper
    return decorate

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    @app.route('/', methods=(['GET']))
    def welcome():
        return b"Hello world!"

    @app.route('/digits/sum', methods=(['POST']))
    @validate_json([
        lambda json: (
            any(map(lambda v: type(v) != str, json["address"]["colorKeys"])),
            "some of colorKeys were not type str"
        ),
        lambda json: (
            any(map(lambda v: type(v) != int, json["address"]["values"])),
            "some of values were not type int"
        ),
        lambda json: (
            type(json["meta"]["digits"]) != int,
            "digits should be type int"
        ),
        lambda json: (
            type(json["meta"]["processingPattern"]) != str,
            "processingPattern should be type str"),
    ])
    def digits_sum():
        values_sum = sum(request.json["address"]["values"])
        digits_iter = map(int, str(values_sum))
        result = sum(digits_iter)
        return jsonify({"result": result})

    return app
