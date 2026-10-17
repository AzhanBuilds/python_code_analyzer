import os
import subprocess
from unittest.mock import patch
import pytest
from backend.app import create_app
from backend.config import TestingConfig
from backend.database import db
from backend.models import User

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        user = User(email="security_tester@example.com", display_name="Security Tester")
        user.set_password("SecurePass123!")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user_id"] = user_id
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_mandatory_security_no_code_execution(client):
    """
    PRD Section 19.4 Mandatory Security Test:
    Verify that user submitted code is NEVER executed, evaluated, or passed to subprocess/system calls.
    """
    malicious_code = """
import os
import subprocess
os.system("echo SHOULD_NOT_RUN")
subprocess.run(["echo", "SHOULD_NOT_RUN"])
"""
    # Mock os.system, subprocess.run, subprocess.Popen, os.popen
    with patch("os.system") as mock_os_system, \
         patch("subprocess.run") as mock_sub_run, \
         patch("subprocess.Popen") as mock_sub_popen, \
         patch("os.popen") as mock_os_popen:

        res = client.post("/api/analyze", json={"code": malicious_code})

        # Ensure response is valid HTTP 200
        assert res.status_code == 200
        data = res.get_json()
        assert data["status"] == "success"
        assert data["valid"] is True

        # Verify absolutely NO execution occurred
        mock_os_system.assert_not_called()
        mock_sub_run.assert_not_called()
        mock_sub_popen.assert_not_called()
        mock_os_popen.assert_not_called()

def test_eval_exec_not_called(client):
    """Verify code containing eval or exec syntax is parsed purely as AST."""
    code = "eval('1 + 1')\nexec('a = 5')\n"
    res = client.post("/api/analyze", json={"code": code})
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    # Variables a=5 should not exist in python globals or locals
    assert "a" not in globals()
