"""
Experiment 18: Pytest Unit Test Suite for Jenkins CI Pipeline
Author: Angulakshmi S (Reg No: 192524402)
"""

import pytest
from app import app

def test_home():
    """Verify that root endpoint returns HTTP 200 and success banner."""
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Jenkins" in resp.data
    assert b"Angulakshmi S" in resp.data

def test_health():
    """Verify that health endpoint returns status UP."""
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    json_data = resp.get_json()
    assert json_data["status"] == "UP"
    assert json_data["pipeline"] == "Jenkins CI/CD"
