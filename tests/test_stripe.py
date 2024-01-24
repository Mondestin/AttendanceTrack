from fastapi.testclient import TestClient
from main import app
from database.firebase import db
from firebase_admin import auth
from dotenv import dotenv_values
import os
import stripe

# Set the TESTING environment variable to 'True'
os.environ['TESTING'] = 'True'

# Create a TestClient instance for making HTTP requests
client = TestClient(app)

# Set up the Stripe test secret API key
config = dotenv_values(".env")
stripe.api_key = config['STRIPE_SK']

# Test case to check if stripe_checkout endpoint redirects successfully
def test_stripe_checkout_redirect():
    response = client.get("/stripe/checkout")
    assert response.status_code == 307  # Redirect status code

# Test case for the success endpoint
def test_stripe_success():
    response = client.get("/stripe/success")
    assert response.status_code == 200
    assert response.json() == {"message": "You have successfully subscribed to Attendance Track"}

# Test case to check if webhook endpoint returns success for a sample event
def test_stripe_webhook_received_success():
    event_data = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "customer_email": "test@example.com"
            }
        }
    }
    response = client.post("/stripe/webhook", json=event_data, headers={"Stripe-Signature": "sample_signature"})
    assert response.status_code == 200




