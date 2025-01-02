import pytest
from conftest import client, setup_database

# GET /personals endpoint'i için test
def test_fetch_personals_data(setup_database):
    # Önce token al
    login_data = {"username": "admin", "password": "admin123"}
    token_response = client.post("/token", data=login_data)
    token = token_response.json()["access_token"]

    # Token ile personel verilerini getir
    response = client.get("/personals", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json()["personals"], list)  # Verilerin bir liste olarak döndüğünü kontrol et