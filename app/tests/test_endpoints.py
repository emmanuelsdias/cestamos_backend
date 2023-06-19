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

def test_get_recipes():
    client = TestClient(app)
    response = client.get("/recipe/")
    #body = response.json()
    assert response.status_code == 403

def test_edit_recipe():
    client = TestClient(app)
    response = client.put("/recipe/1")
    #body = response.json()
    assert response.status_code == 422



#*****************************************************    
#Item
def test_edit_item():
    client = TestClient(app)
    response = client.put("/item/1")
    #body = response.json()
    assert response.status_code == 422


#User
def test_get_user():
    client = TestClient(app)
    response = client.get("/user/")
    #body = response.json()
    assert response.status_code == 200

def test_edit_user():
    client = TestClient(app)
    response = client.put("/user/1")
    #body = response.json()
    assert response.status_code == 405

#Invitation
def test_get_invitation():
    client = TestClient(app)
    response = client.get("/invitation/")
    #body = response.json()
    assert response.status_code == 403

#Friendship
def test_get_friendship():
    client = TestClient(app)
    response = client.get("/friendship/")
    #body = response.json()
    assert response.status_code == 403



#List
def test_get_list():
    client = TestClient(app)
    response = client.get("/list/")
    #body = response.json()
    assert response.status_code == 404

def test_edit_list():
    client = TestClient(app)
    response = client.put("/list/1")
    #body = response.json()
    assert response.status_code == 404

#UserList
def test_edit_user_list():
    client = TestClient(app)
    response = client.put("/user_list/1")
    #body = response.json()
    assert response.status_code == 422
