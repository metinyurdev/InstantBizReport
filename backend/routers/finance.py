from fastapi import APIRouter, Depends
from security.auth import get_current_user
from models.database import get_db
from models.tables import finance_table
from sqlalchemy import select
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Matplotlib backend'ini ayarla
import matplotlib
matplotlib.use('agg')

router = APIRouter()

@router.get("/finance")
def get_finance(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    query = select(finance_table)
    results = db.execute(query).fetchall()
    finance_data = [dict(row._mapping) for row in results]
    return {"finance": finance_data}

@router.get("/finance/plot")
def plot_finance(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    query = select(finance_table)
    results = db.execute(query).fetchall()

    data = pd.DataFrame(results, columns=['id', 'category', 'amount', 'record_date'])
    data['amount'] = pd.to_numeric(data['amount'], errors='coerce')
    data.dropna(subset=['amount'], inplace=True)

    if data['amount'].isnull().all():
        return {"error": "No numeric data to plot"}

    if data.empty:
        return {"error": "No data available to plot"}
    if not data['amount'].dtype.kind in 'fi':
        return {"error": "Amount field is not numeric"}

    plt.figure(figsize=(8, 6))
    data.groupby("category")["amount"].sum().plot(kind="bar", color=["green", "red"])
    plt.title("Finance Overview")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
