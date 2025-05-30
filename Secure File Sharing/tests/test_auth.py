from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_login():
    email = "testuser@example.com"
    password = "testpass"
    role = "client"

    r = client.post("/auth/signup", params={"email": email, "password": password, "role": role})
    assert r.status_code == 200

    r = client.post("/auth/login", params={"email": email, "password": password})
    assert r.status_code == 200
    assert "access_token" in r.json()
