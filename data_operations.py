from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Vendedor, Cliente

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_todos_vendedores():
    db = SessionLocal()
    try:
        vendedores = db.query(Vendedor).all()
        return vendedores
    finally:
        db.close()

def get_todos_clientes():
    db = SessionLocal()
    try:
        clientes = db.query(Cliente).all()
        return clientes
    finally:
        db.close()