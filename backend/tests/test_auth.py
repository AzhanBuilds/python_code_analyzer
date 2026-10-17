import pytest
from backend.app import create_app
from backend.config import TestingConfig
from backend.database import db
from backend.models import User

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_success(client):
    """Test successful user registration."""
    payload = {
        "email": "alice@example.com",
        "display_name": "Alice Dev",
        "password": "StrongPassword123!"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["status"] == "success"
    assert "user" in data
    assert data["user"]["email"] == "alice@example.com"
    assert data["user"]["display_name"] == "Alice Dev"
    # Security requirement: password_hash must NEVER be returned
    assert "password_hash" not in data["user"]
    assert "password" not in data["user"]

    # Verify session is established
    with client.session_transaction() as sess:
        assert sess.get("user_id") is not None

def test_register_duplicate_email(client):
    """Test registration failure when email already exists (case-insensitive)."""
    payload = {
        "email": "bob@example.com",
        "display_name": "Bob Builder",
        "password": "StrongPassword123!"
    }
    res1 = client.post("/api/auth/register", json=payload)
    assert res1.status_code == 201

    # Attempt to register again with same email in upper/mixed case
    duplicate_payload = {
        "email": "BOB@example.com",
        "display_name": "Bob Duplicate",
        "password": "AnotherPassword456!"
    }
    res2 = client.post("/api/auth/register", json=duplicate_payload)
    assert res2.status_code == 409
    data2 = res2.get_json()
    assert data2["status"] == "error"
    assert "already exists" in data2["error"].lower()

def test_register_missing_fields(client):
    """Test registration validation with missing fields."""
    res1 = client.post("/api/auth/register", json={"email": "incomplete@example.com"})
    assert res1.status_code == 400
    assert "missing" in res1.get_json()["error"].lower()

    res2 = client.post("/api/auth/register", json={})
    assert res2.status_code == 400

def test_register_invalid_email(client):
    """Test email syntax validation."""
    payload = {
        "email": "invalid-email-format",
        "display_name": "Invalid Email User",
        "password": "StrongPassword123!"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 400
    assert "email" in res.get_json()["error"].lower()

def test_register_weak_password(client):
    """Test password strength validation on registration."""
    # Too short (< 8 chars)
    payload_short = {
        "email": "short@example.com",
        "display_name": "Short Pwd",
        "password": "Short1!"
    }
    res = client.post("/api/auth/register", json=payload_short)
    assert res.status_code == 400
    assert "8 characters" in res.get_json()["error"].lower()

    # Missing uppercase letter
    payload_no_upper = {
        "email": "noupper@example.com",
        "display_name": "No Upper",
        "password": "lowercase123!"
    }
    res = client.post("/api/auth/register", json=payload_no_upper)
    assert res.status_code == 400
    assert "uppercase" in res.get_json()["error"].lower()

def test_login_success(client):
    """Test successful user login."""
    # First register user
    client.post("/api/auth/register", json={
        "email": "carol@example.com",
        "display_name": "Carol Danvers",
        "password": "MarvelPassword2026!"
    })

    # Clear session to simulate fresh login
    client.post("/api/auth/logout")

    # Login
    login_res = client.post("/api/auth/login", json={
        "email": "carol@example.com",
        "password": "MarvelPassword2026!"
    })
    assert login_res.status_code == 200
    data = login_res.get_json()
    assert data["status"] == "success"
    assert data["user"]["email"] == "carol@example.com"
    assert "password_hash" not in data["user"]

def test_login_incorrect_password(client):
    """Test login failure with wrong password."""
    client.post("/api/auth/register", json={
        "email": "dan@example.com",
        "display_name": "Dan User",
        "password": "CorrectPassword123!"
    })

    res = client.post("/api/auth/login", json={
        "email": "dan@example.com",
        "password": "WrongPassword999!"
    })
    assert res.status_code == 401
    data = res.get_json()
    assert data["status"] == "error"
    # Verify generic message prevents user enumeration
    assert "invalid email or password" in data["error"].lower()

def test_login_nonexistent_user(client):
    """Test login failure with unknown email address."""
    res = client.post("/api/auth/login", json={
        "email": "ghost@example.com",
        "password": "SomePassword123!"
    })
    assert res.status_code == 401
    assert "invalid email or password" in res.get_json()["error"].lower()

def test_current_user_endpoint(client):
    """Test GET /api/auth/me for authenticated and unauthenticated states."""
    # 1. Unauthenticated request must return 401
    unauth_res = client.get("/api/auth/me")
    assert unauth_res.status_code == 401

    # 2. Authenticate
    client.post("/api/auth/register", json={
        "email": "me_user@example.com",
        "display_name": "Me Tester",
        "password": "MePassword123!"
    })

    # 3. Authenticated request must return 200 and user data
    auth_res = client.get("/api/auth/me")
    assert auth_res.status_code == 200
    user_data = auth_res.get_json()["user"]
    assert user_data["email"] == "me_user@example.com"
    assert user_data["display_name"] == "Me Tester"
    assert "password_hash" not in user_data

def test_logout(client):
    """Test user logout clears active session."""
    client.post("/api/auth/register", json={
        "email": "logout_test@example.com",
        "display_name": "Logout Tester",
        "password": "LogoutPassword123!"
    })

    # Should be authenticated
    me_res = client.get("/api/auth/me")
    assert me_res.status_code == 200

    # Logout
    logout_res = client.post("/api/auth/logout")
    assert logout_res.status_code == 200

    # Should no longer be authenticated
    me_after = client.get("/api/auth/me")
    assert me_after.status_code == 401

def test_protected_endpoints_enforcement(client):
    """Verify that protected backend endpoints reject unauthenticated requests and accept authenticated ones."""
    # Unauthenticated /api/analyze should return 401
    unauth_analyze = client.post("/api/analyze", json={"code": "x = 1\n"})
    assert unauth_analyze.status_code == 401
    assert "authentication required" in unauth_analyze.get_json()["error"].lower()

    # Authenticate
    client.post("/api/auth/register", json={
        "email": "analyzer_user@example.com",
        "display_name": "Analyzer User",
        "password": "AnalyzePass123!"
    })

    # Authenticated /api/analyze should succeed with 200
    auth_analyze = client.post("/api/analyze", json={"code": "x = 1\n"})
    assert auth_analyze.status_code == 200
    assert auth_analyze.get_json()["status"] == "success"
