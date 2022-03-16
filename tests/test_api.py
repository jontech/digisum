import json
from flaskr import create_app

def test_digits_sum_ok_result(client):
    """Should respond with result of digits sum from sum of values in test data"""
    test_data = {
        "address": {
            "colorKeys": ["A", "G", "Z"],
            "values": [74, 117, 115, 116, 79, 110]
        },
        "meta": {
            "digits": 33,
            "processingPattern": "d{5}+[a-z&$§]"
        }
    }
    response = client.post('/digits/sum', json=test_data)
    assert response.status_code == 200
    assert json.loads(response.data)["result"] == 8 

def test_digits_sum_invalid_data(client):
    """Should respond with errors for each invalid field"""
    test_data = {
        "address": {
            "colorKeys": [1, 2, 3],
            "values": ["1", "2"]
        },
        "meta": {
            "digits": True,
            "processingPattern": None
        }
    }
    response = client.post('/digits/sum', json=test_data)
    assert response.status_code == 400

def test_digits_sum_malformed_json(client):
    """Should respond with bad request when invalid json"""
    test_data = "{"
    response = client.post('/digits/sum', json=test_data)
    assert response.status_code == 400

def test_digits_sum_missing_json_keys(client):
    """Should respond with bad request when missing keys in json"""
    test_data = {
        "address": {},
        "meta": {}
    }
    response = client.post('/digits/sum', json=test_data)
    assert response.status_code == 400
    
def test_digits_sum_missing_json_header(client):
    """Should respond with bad request when request body is not json"""
    response = client.post('/digits/sum', data="oh no")
    assert response.status_code == 400
    
