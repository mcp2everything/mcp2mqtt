import pytest
from mcp2mqtt.server import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

def test_set_pwm_endpoint(app):
    with app.test_client() as client:
        # Test valid request
        response = client.post('/set-pwm', json={'frequency': 50})
        assert response.status_code == 200
        assert response.json['status'] == 'success'

        # Test invalid frequency
        response = client.post('/set-pwm', json={'frequency': 101})
        assert response.status_code == 400
        assert 'error' in response.json

        # Test missing frequency parameter
        response = client.post('/set-pwm', json={})
        assert response.status_code == 400
        assert 'error' in response.json
