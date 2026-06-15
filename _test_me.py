import json
import urllib.request
import urllib.error

BASE = "http://localhost:5000"

# Login to get token
data = json.dumps({"email": "test@test.com", "password": "test123"}).encode()
req = urllib.request.Request(f"{BASE}/api/v1/auth/login", data=data, method="POST")
req.add_header("Content-Type", "application/json")
resp = urllib.request.urlopen(req)
body = json.loads(resp.read())
token = body["data"]["access_token"]

# Test /me with token
req2 = urllib.request.Request(f"{BASE}/api/v1/auth/me", method="GET")
req2.add_header("Authorization", f"Bearer {token}")
try:
    resp2 = urllib.request.urlopen(req2)
    print(f"  {resp2.status}  {resp2.read().decode()}")
except urllib.error.HTTPError as e:
    print(f"  {e.code}  {e.read().decode()}")
