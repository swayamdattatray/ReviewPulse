import json
import urllib.request

BASE = "http://localhost:5000"

def post(path, data):
    url = BASE + path
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    resp = urllib.request.urlopen(req)
    return resp.status, json.loads(resp.read())

def get(path, token=None):
    url = BASE + path
    req = urllib.request.Request(url, method="GET")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    resp = urllib.request.urlopen(req)
    return resp.status, json.loads(resp.read())

# 1. Register
print("--- POST /api/v1/auth/register ---")
code, body = post("/api/v1/auth/register", {
    "username": "testuser",
    "email": "test@test.com",
    "password": "test123",
    "first_name": "Test",
    "last_name": "User",
})
print(f"  {code}  success={body['success']}  user={body['data']['user']['username']}")

# 2. Login
print("\n--- POST /api/v1/auth/login ---")
code, body = post("/api/v1/auth/login", {
    "email": "test@test.com",
    "password": "test123",
})
token = body["data"]["access_token"]
print(f"  {code}  success={body['success']}  token={token[:20]}...")

# 3. Get profile
print("\n--- GET /api/v1/auth/me ---")
code, body = get("/api/v1/auth/me", token=token)
print(f"  {code}  success={body['success']}  user={body['data']['user']['email']}")
