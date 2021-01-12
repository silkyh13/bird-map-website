import os
import tempfile
import pytest
import random
import json
from datetime import datetime

from app import app
 
@pytest.fixture
def client():
   with app.test_client() as client:
       with app.app_context():
           pass
       yield client
 
class TestApp:
 
    def test_get_birds(self, client):
        response = client.get('/bird')
        print(json.dumps(response.data))
        assert 'data' in response.data
    
    def test_post_bird(self, client):
        now = datetime.now()
        test_id = now.strftime("%Y-%m-%d--%H-%M-%S")

        response = client.post('/bird', json={
            "id": "test-id-{}".format(test_id),
            "name": "Test Bird #{}".format(test_id),
           'image': "bird.image",
           'description': "bird.description",
           'life_history': "bird.life_history",
           'distribution_and_habitat': "bird.distribution_and_habitat",
           'status': "bird.status",
           'management_and_research_needs': "bird.management_and_research_needs",
           'locations': ['stuff', 'hello']
        })
        assert 'success' in response.data
    
    def test_get_specific_bird(self, client):
        response = client.get('/bird/american-bittern')
        print('hehe',response.data)
    
    def test_update_specific_bird(self, client):
        response = client.put('/bird/black-tern', json={
            "name":'DOES IT WORK',
            'image': "bird.image",
            'description': "bird.description",
            'life_history': "bird.life_history",
            'distribution_and_habitat': "bird.distribution_and_habitat",
            'status': "bird.status",
            'management_and_research_needs': "bird.management_and_research_needs",
            'locations': ['stuff', 'hello']
        })
        assert 'id' in response.data