import pytest
from backend.app import create_app
from backend.config import Config

class TestConfig(Config):
    TESTING = True
    MAX_SOURCE_LENGTH = 1000

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "python-code-analyzer"

def test_analyze_successful(client):
    payload = {"code": "def hello():\n    return 'world'\n"}
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["valid"] is True
    assert data["metrics"]["functions"] == 1
    assert "quality_score" in data
    assert "summary" in data

def test_analyze_missing_code_field(client):
    res = client.post("/api/analyze", json={})
    assert res.status_code == 400
    data = res.get_json()
    assert data["status"] == "error"

def test_analyze_code_not_a_string(client):
    res = client.post("/api/analyze", json={"code": 12345})
    assert res.status_code == 400
    data = res.get_json()
    assert data["status"] == "error"

def test_analyze_non_json(client):
    res = client.post("/api/analyze", data="plain text", content_type="text/plain")
    assert res.status_code == 400

def test_analyze_syntax_error(client):
    res = client.post("/api/analyze", json={"code": "def bad_syntax(:"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "syntax_error"
    assert data["valid"] is False
    assert data["quality_score"] is None
    assert data["syntax_error"] is not None
    assert "line" in data["syntax_error"]

def test_analyze_payload_too_large(client):
    huge_code = "a = 1\n" * 500  # > 1000 chars
    res = client.post("/api/analyze", json={"code": huge_code})
    assert res.status_code == 413
    data = res.get_json()
    assert data["status"] == "error"

def test_trailing_slashes_tolerance(client):
    res_health = client.get("/api/health/")
    assert res_health.status_code == 200

    res_analyze = client.post("/api/analyze/", json={"code": "x = 1\n"})
    assert res_analyze.status_code == 200
    assert res_analyze.get_json()["status"] == "success"

