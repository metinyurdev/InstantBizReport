import sys
import os

# Projenin kök dizinini Python'un modül yollarına ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from models.database import get_db
from models.tables import finance_table, sales_table, personals_table, users_table
from security.auth import create_access_token
from security.hash import get_password_hash
from datetime import timedelta
import os
import sys

# Projenin kök dizinini Python'un modül yollarına ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test veritabanı bağlantısı
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost/proje_test_veritabani"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Test istemcisi
client = TestClient(app)

# Veritabanı bağlantısını override eden fixture
@pytest.fixture
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test öncesi ve sonrası veritabanını yöneten fixture
@pytest.fixture
def setup_database(test_db: Session):
    # Test öncesi veritabanını hazırla
    test_db.execute(finance_table.insert().values(id=10, category="income", amount=1000, record_date="2023-10-01"))
    test_db.execute(sales_table.insert().values(id=10, product="product1", amount=500, sale_date="2023-10-01"))
    test_db.execute(personals_table.insert().values(id=10, name="John", lastname="Doe", age=30, position="Manager", department="HR", email="john.doe@example.com"))
    
    # Kullanıcı şifresini hash'le
    hashed_password = get_password_hash("testpass")
    test_db.execute(users_table.insert().values(id=10, username="testuser", password=hashed_password, email="test@example.com", created_at="2023-10-01"))
    
    test_db.commit()
    yield
    # Test sonrası veritabanını temizle
    test_db.execute(finance_table.delete())
    test_db.execute(sales_table.delete())
    test_db.execute(personals_table.delete())
    test_db.execute(users_table.delete())
    test_db.commit()

# Mock current_user için fixture
@pytest.fixture
def mock_current_user():
    return {"username": "testuser", "email": "test@example.com"}