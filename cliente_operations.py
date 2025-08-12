from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Cliente

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_cliente(dados_cliente: dict):
    
    db = SessionLocal()

    novo_cliente = Cliente (
        nome_cliente = dados_cliente['nome_cliente'],
        endereco = dados_cliente['endereco'],
        telefone = dados_cliente['telefone']
    )

    try:
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        return novo_cliente
    except Exception as e:
        print(f"Erro detalhado ao adicionar cliente: {e}")
        db.rollback()
        return None
    finally:
        db.close()