from databases import Database
from sqlalchemy import create_engine, MetaData

DATA_BASE_URL = "sqlite:///./rpg.db"  

database = Database(DATA_BASE_URL)
engine   = create_engine(DATA_BASE_URL)
metadata = MetaData()
