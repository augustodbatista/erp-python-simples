# populate_db.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Vendedor, Cliente
from datetime import date

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def adicionar_dados_iniciais():
    db = SessionLocal()
    try:
        # Adicionar Vendedores
        if db.query(Vendedor).count() == 0:
            print("Adicionando vendedores iniciais...")
            vendedores = [
                Vendedor(nome_vendedor="Carlos Silva", data_contratacao=date(2023, 1, 15)),
                Vendedor(nome_vendedor="Mariana Costa", data_contratacao=date(2022, 5, 20)),
                Vendedor(nome_vendedor="João Pereira", data_contratacao=date(2023, 3, 10))
            ]
            db.add_all(vendedores)
            db.commit()
            print("Vendedores adicionados.")
        else:
            print("Vendedores já existem.")

        # Adicionar Clientes
        if db.query(Cliente).count() == 0:
            print("Adicionando clientes iniciais...")
            clientes = [
                Cliente(nome_cliente="Padaria Pão Quente", endereco="Rua das Flores, 123", telefone="37999998888"),
                Cliente(nome_cliente="Mercado Central", endereco="Av. Principal, 456", telefone="37988887777"),
                Cliente(nome_cliente="Oficina do Zé", endereco="Rua da Garagem, 789", telefone="37977776666")
            ]
            db.add_all(clientes)
            db.commit()
            print("Clientes adicionados.")
        else:
            print("Clientes já existem.")
            
    finally:
        db.close()

if __name__ == "__main__":
    adicionar_dados_iniciais()