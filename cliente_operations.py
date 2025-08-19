from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Cliente
from database import SessionLocal

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
            return novo_cliente
    except Exception as e:
        return None
