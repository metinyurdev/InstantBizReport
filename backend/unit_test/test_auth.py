import pytest
from conftest import client, setup_database
from datetime import timedelta

# POST /token endpoint'i için test
def test_get_token(setup_database):
    login_data = {"username": "admin", "password": "admin123"}
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()  # Token'ın döndüğünü kontrol et

# GET /users/me endpoint'i için test
def test_fetch_current_user(setup_database):
    # Önce token al
    login_data = {"username": "admin", "password": "admin123"}
    token_response = client.post("/token", data=login_data)
    token = token_response.json()["access_token"]

    # Token ile kullanıcı bilgilerini getir
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["user"] == "admin"  # Kullanıcı bilgilerinin doğru döndüğünü kontrol et

# POST /logout endpoint'i için test
def test_logout(setup_database):
    # Önce token al
    login_data = {"username": "admin", "password": "admin123"}
    token_response = client.post("/token", data=login_data)
    token = token_response.json()["access_token"]

    # Logout işlemi
    response = client.post("/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}