import json
import urllib.request
import urllib.error

BASE = "http://localhost:5000"

endpoints = [
    ("GET",  "/api/v1/"),
    ("GET",  "/api/v1/health"),
    ("GET",  "/api/v1/products"),
    ("GET",  "/api/v1/products/1"),
    ("GET",  "/api/v1/products/categories"),
    ("GET",  "/api/v1/reviews"),
    ("GET",  "/api/v1/reviews/1"),
    ("GET",  "/api/v1/analytics/dashboard"),
    ("GET",  "/api/v1/trends/category"),
    ("GET",  "/api/v1/trends/product/1"),
    ("POST", "/api/v1/auth/register"),
    ("POST", "/api/v1/auth/login"),
    ("GET",  "/api/v1/auth/me"),
]

for method, path in endpoints:
    url = BASE + path
    try:
        req = urllib.request.Request(url, method=method)
        if method == "POST":
            data = json.dumps({}).encode()
            req.add_header("Content-Type", "application/json")
            req.data = data
        resp = urllib.request.urlopen(req)
        body = json.loads(resp.read())
        status = resp.status
        ok = body.get("success", False)
        print(f"  {status}  {'OK' if ok else 'FAIL':4s}  {method:4s} {path}")
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        print(f"  {e.code}  FAIL  {method:4s} {path}  -> {body.get('error', '?')}")
    except Exception as e:
        print(f"  ERR   FAIL  {method:4s} {path}  -> {e}")
