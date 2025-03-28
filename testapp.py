# Write tests to tests the app endpoints

# Test the FastAPI application endpoints using pytest and httpx
import pytest
from fastapi.testclient import TestClient
from app import app  # Import your FastAPI app here


# Create a test client for the FastAPI app
client = TestClient(app)

# Test case for the root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI WebSocket server!"}

# Test case for the WebSocket endpoint
def test_websocket_endpoint():
    with client.websocket_connect("/ws") as websocket:
        # Send a message to the WebSocket server
        websocket.send_text("Hello, WebSocket!")
        
        # Receive a message from the WebSocket server
        data = websocket.receive_text()
        
        # Assert that the received message is as expected
        assert data == "Hello, WebSocket!"  # Adjust this based on your actual implementation
        # You can also check the type of data received if needed

# run tests
if __name__ == "__main__":
    pytest.main(["-v", "testapp.py"])
