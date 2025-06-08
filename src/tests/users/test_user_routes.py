import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from users.user_routes import users_blueprint


# create a test client
@pytest.fixture
def app():
  app = Flask(__name__)
  app.register_blueprint(users_blueprint, url_prefix='/users')
  
  # mock the MongoDB connection
  app.config["db"] = {"users": MagicMock()}
  return app

@pytest.fixture
def client(app):
  return app.test_client()


def test_create_user_success():
  # Arrange
  user_data = {"name": "John Doe", "email": "qo0k7@example.com", "password": "password123"}
  
  # Act
  mock_result = MagicMock()
  mock_result.inserted_id = "123"
  app.config["db"]["users"].insert_one.return_value = mock_result
  
  response = client.post('/users', json=user_data)
  
  # Assert
  assert response.status_code == 201
  assert response.json()["message"] == "User created successfully"
  assert response.json()["id"] == "123"
  app.config["db"]["users"].insert_one.assert_called_once_with(user_data)
  
  # Clean up
  app.config["db"]["users"].insert_one.reset_mock()
  

def test_create_user_invalid_data():
  # Arrange
  invalid_data = {"name": "John Doe", "email": "invalid_email", "password": "password123"}
  
  # Act
  response = client.post('/users/', json=invalid_data)
  
  # Assert
  assert response.status_code == 400
  assert "error" in response.json()
  
  # Clean up
  app.config["db"]["users"].insert_one.reset_mock()