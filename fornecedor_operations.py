from models import Fornecedor
from database import SessionLocal

def add_fornecedor(dados_fornecedor: dict):
    
    novo_fornecedor = Fornecedor (
        nome_fornecedor = dados_fornecedor['nome_fornecedor'],
        cpf_cnpj = dados_fornecedor['cpf_cnpj'],
        endereco = dados_fornecedor['endereco'],
        telefone = dados_fornecedor['telefone']
    )

    try:
        with SessionLocal() as db:
            db.add(novo_fornecedor)
            db.commit()
            db.refresh(novo_fornecedor)
            return novo_fornecedor
    except Exception as e:
            return None