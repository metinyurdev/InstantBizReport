from fastapi import APIRouter, Depends
from security.auth import get_current_user
from models.database import get_db
from models.tables import finance_table
from sqlalchemy import select

router = APIRouter()

@router.get("/finance")
def get_finance(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    query = select(finance_table)
    results = db.execute(query).fetchall()
    finance_data = [dict(row._mapping) for row in results]
    return {"finance": finance_data}


