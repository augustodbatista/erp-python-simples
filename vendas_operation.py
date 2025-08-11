from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Venda
from datetime import date

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_venda(dados_venda: dict):
    """
    Adiciona uma nova venda ao banco de dados.
    'dados_venda' é um dicionário esperado com as chaves:
    'data_venda', 'valor_total', 'pago', 'forma_pagamento',
    'data_vencimento', 'cliente_id', 'vendedor_id'
    """
    db = SessionLocal()
    
    nova_venda = Venda(
        data_venda=dados_venda['data_venda'],
        numero_notinha=dados_venda['numero_notinha'],
        valor_total=dados_venda['valor_total'],
        pago=dados_venda['pago'],
        forma_pagamento=dados_venda['forma_pagamento'],
        data_vencimento=dados_venda.get('data_vencimento'), # .get() é mais seguro para campos opcionais
        cliente_id=dados_venda['cliente_id'],
        vendedor_id=dados_venda['vendedor_id']
    )

    try:
        db.add(nova_venda)
        db.commit()
        db.refresh(nova_venda)
        print(f"Venda ID {nova_venda.id} adicionada com sucesso!")
        return nova_venda
    except Exception as e:
        print(f"Erro ao adicionar venda: {e}")
        db.rollback()
        return None
    finally:
        db.close()