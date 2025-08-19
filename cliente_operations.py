from models import Cliente
from database import SessionLocal
import logging

def add_cliente(dados_cliente: dict):

    novo_cliente = Cliente (
        nome_cliente = dados_cliente['nome_cliente'],
        endereco = dados_cliente['endereco'],
        telefone = dados_cliente['telefone']
    )

    try:
        with SessionLocal() as db:
            db.add(novo_cliente)
            db.commit()
            db.refresh(novo_cliente)
            logging.info(f"Cliente '{novo_cliente.nome_cliente}' (ID: {novo_cliente.id}) adicionado com sucesso.")
            return novo_cliente
    except Exception as e:
        logging.error(f"Erro ao adicionar cliente '{dados_cliente['nome_cliente']}': {e}")
        return None
