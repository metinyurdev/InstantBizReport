from sqlalchemy import Table
from .database import metadata, engine

# Tablo referansları 
users_table = Table('users', metadata, autoload_with=engine) 
sales_table = Table('sales', metadata, autoload_with=engine) 
personals_table = Table('personals', metadata, autoload_with=engine) 
finance_table = Table('finance', metadata, autoload_with=engine)
