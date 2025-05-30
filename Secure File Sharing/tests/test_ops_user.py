from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ops_upload_file():
    email = "ops@example.com"
    password = "securepass"

    # Signup
    client.post("/auth/signup", params={
        "email": email,
        "password": password,
        "role": "ops"
    })

    # Login
    response = client.post("/auth/login", params={
        "email": email,
        "password": password
    })
    token = response.json()["access_token"]

    # Upload file
    files = {'file': ('example.docx', b"fake content")}
    res = client.post("/ops/upload", files=files, headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200
    assert "filename" in res.json()
