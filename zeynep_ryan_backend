from fastapi import APIRouter, Depends
from security.auth import get_current_user
from models.database import get_db
from models.tables import personals_table
from sqlalchemy import select

router = APIRouter()

@router.get("/personals")
def get_personals(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    query = select(personals_table)
    results = db.execute(query).fetchall()
    return {"personals": [dict(row._mapping) for row in results]}
