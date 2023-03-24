"""Test Suite for the app.py module"""
import json
import pytest
from app import app
from src.service import AuthService

test = app.test_client()

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert json.loads(response.data) == {"message": "Hello World!"}
    
def test_consent_screen(client):
    response = client.get("/api/")
    assert response.status_code == 302

def test_healthcheck(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert json.loads(response.data) == {"message": "Stack is healthy", "status": "success"}
    
def test_callback(client):
    response = client.get("/api/callback?code=test_code")
    assert response.status_code == 200
    assert json.loads(response.data) == {"message": "Processing images"}

def test_rabbitmq(client):
    response = client.get("/dashboards/rabbitmq")
    assert response.status_code == 302
    assert response.headers["location"] == "http://localhost:15672"

def test_minio(client):
    response = client.get("/dashboards/minio")
    assert response.status_code == 302
    assert response.headers["location"] == "http://localhost:9001"