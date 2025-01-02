import pytest
from conftest import client, setup_database

# GET /finance endpoint'i için test
def test_fetch_finance_data(setup_database):
    # Önce token al
    login_data = {"username": "admin", "password": "admin123"}
    token_response = client.post("/token", data=login_data)
    token = token_response.json()["access_token"]

    # Token ile finans verilerini getir
    response = client.get("/finance", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json()["finance"], list)  # Verilerin bir liste olarak döndüğünü kontrol et

# GET /finance/plot endpoint'i için test
def test_plot_finance(setup_database):
    # Önce token al
    login_data = {"username": "admin", "password": "admin123"}
    token_response = client.post("/token", data=login_data)
    token = token_response.json()["access_token"]

    # Token ile finans görselini getir
    response = client.get("/finance/plot", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"  # Görselin PNG formatında döndüğünü kontrol et