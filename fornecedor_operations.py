from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Fornecedor

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_fornecedor(dados_fornecedor: dict):
    
    db = SessionLocal()

    novo_fornecedor = Fornecedor (
        nome_fornecedor = dados_fornecedor['nome_fornecedor'],
        cpf_cnpj = dados_fornecedor['cpf_cnpj'],
        endereco = dados_fornecedor['endereco'],
        telefone = dados_fornecedor['telefone']
    )

    try:
        db.add(novo_fornecedor)
        db.commit()
        db.refresh(novo_fornecedor)
        return novo_fornecedor
    except Exception as e:
        print(f"Erro detalhado ao adicionar fornecedor: {e}")
        db.rollback()
        return None
    finally:
        db.close()