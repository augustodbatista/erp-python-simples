from sqlalchemy import create_engine
from models import Base, Vendedor, Cliente, Usuario 

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL, echo=True)
print("Iniciando a criação das tabelas no banco de dados...")
Base.metadata.create_all(engine)
print("Tabelas criadas com sucesso!")