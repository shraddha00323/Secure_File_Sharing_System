from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_client_signup_and_list_files():
    email = "client@example.com"
    password = "test123"

    # Signup
    client.post("/auth/signup", params={
        "email": email,
        "password": password,
        "role": "client"
    })

    # Login
    response = client.post("/auth/login", params={
        "email": email,
        "password": password
    })
    token = response.json()["access_token"]

    # List files
    res = client.get("/client/list-files", headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
    assert isinstance(res.json()["files"], list)
