import json
from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_digit_sum_result_api(client):
    """Should respond with result of digit sum from sum of values in test data"""
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
    response = client.post('/digits/sum', data=json.dumps(test_data))
    assert response.status_code == 200
    assert json.loads(response.data)["result"] == 8 

def test_digit_sum_api_invalid_data(client):
    """Should respond with bad request when invalid json"""
    test_data = "{"
    response = client.post('/digits/sum', data=json.dumps(test_data))
    assert response.status_code == 400
