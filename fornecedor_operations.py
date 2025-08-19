from models import Fornecedor
from database import SessionLocal
import logging

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
            logging.info(f"Fornecedor '{novo_fornecedor.nome_fornecedor}' (ID: {novo_fornecedor.id}) adicionado com sucesso.")
            return novo_fornecedor
    except Exception as e:
            logging.error(f"Erro ao adicionar fornecedor '{dados_fornecedor['nome_fornecedor']}': {e}")
            return None