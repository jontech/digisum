import os
import json
from functools import wraps
from flask import Flask, jsonify, request

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='$JKJFAK541048635',
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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
    
    @app.route('/digits/sum', methods=(['POST']))
    @as_json
    def digits_sum(data):
        values_sum = sum(data["address"]["values"])
        digits_iter = map(int, str(values_sum))
        result = sum(digits_iter)
        return {"result": result}

    return app
