from database import engine
from models import Base

print("Iniciando a criação das tabelas no banco de dados...")
Base.metadata.create_all(engine)
print("Tabelas criadas com sucesso!")