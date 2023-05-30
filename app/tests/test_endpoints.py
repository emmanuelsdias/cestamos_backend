from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from starlette.testclient import TestClient

from main import app

def test_get_all_users():
    client = TestClient(app)
    response = client.get("/user/")
    #body = response.json()
    assert response.status_code == 200
