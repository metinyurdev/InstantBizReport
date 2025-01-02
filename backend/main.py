from fastapi import FastAPI
import uvicorn
from routers import user, sales, personal, finance

app = FastAPI()

app.include_router(user.router)
app.include_router(sales.router)
app.include_router(personal.router)
app.include_router(finance.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
