from fastapi import APIRouter, Depends
from security.auth import get_current_user
from models.database import get_db
from models.tables import sales_table
from sqlalchemy import select

router = APIRouter()

@router.get("/sales")
def get_sales(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    query = select(sales_table)
    results = db.execute(query).fetchall()
    return {"sales": [dict(row._mapping) for row in results]}
