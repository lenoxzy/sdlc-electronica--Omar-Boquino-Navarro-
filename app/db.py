from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 1. Calculamos la ruta raíz de tu proyecto dinámicamente
# __file__ es db.py, .parent es app/, .parent.parent es tu carpeta raíz
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Le decimos a SQLite que SIEMPRE lo guarde en esa raíz
SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}/sensorhub.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass