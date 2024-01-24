# Import necessary modules
from firebase_admin import auth
from fastapi.testclient import TestClient
from main import app
import pytest

# Set the TESTING environment variable to 'True'
import os
os.environ['TESTING'] = 'True'

# Create a TestClient instance
client = TestClient(app)

# Define a fixture to clean up resources after testing
@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    # Define a function to remove test users from Firebase
    def remove_test_users():
        users = auth.list_users().iterate_all()
        for user in users:
            if user.email.startswith("test."):
                auth.delete_user(user.uid)
    # Add the cleanup function to the finalizer, ensuring it runs after all tests
    request.addfinalizer(remove_test_users)

# Define a fixture to create a test user during testing
@pytest.fixture
def create_user():
    user_credential = client.post("/auth/signup", json={
        "email": "test.user2@gmail.com", 'password': "password"
    })

# Define a fixture to authenticate a test user during testing
@pytest.fixture
def auth_user(create_user):
    user_credential = client.post("/auth/login", data={
        "username": "test.user2@gmail.com",
        "password": "password",
    })
    # Return the user credentials in JSON format
    return user_credential.json()
