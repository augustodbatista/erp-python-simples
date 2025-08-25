from sqlalchemy.orm import joinedload
from database import SessionLocal
from models import Vendedor, Cliente, Fornecedor, Pagamento, Venda
import logging


def get_todos_vendedores():
    try:
        with SessionLocal() as db:
            vendedores = db.query(Vendedor).all()
            return vendedores
    except Exception as e:
        logging.error(f"Erro ao buscar todos os vendedores: {e}")
        return []

def get_todos_clientes():
    try:
        with SessionLocal() as db:
            clientes = db.query(Cliente).all()
            return clientes
    except Exception as e:
        logging.error(f"Erro ao buscar todos os cliente: {e}")
        return []

def search_clientes_por_nome(termo_busca: str):
    try:
        with SessionLocal() as db:
            search_clientes = db.query(Cliente).filter(Cliente.nome_cliente.ilike(f'%{termo_busca}%')).all()
            return search_clientes
    except Exception as e:
        logging.error(f"Erro ao buscar cliente pelo termo'{termo_busca}': {e}")
        return []

def search_fornecedores_por_nome(termo_busca: str):
    try:
        with SessionLocal() as db:
            search_fornecedores = db.query(Fornecedor).filter(Fornecedor.nome_fornecedor.ilike(f'%{termo_busca}%')).all()
            return search_fornecedores
    except Exception as e:
        logging.error(f"Erro ao buscar fornecedor pelo termo'{termo_busca}': {e}")
        return []


def search_vendas_nao_pagas(termo_busca: str):
    try:
        with SessionLocal() as db:
            from models import Venda, Cliente
        
            query = db.query(Venda).options(joinedload(Venda.cliente)).filter(Venda.pago == False)

            if termo_busca.isdigit(): 
                query = query.filter(Venda.numero_notinha == int(termo_busca))
            else: 
                query = query.join(Cliente).filter(Cliente.nome_cliente.ilike(f'%{termo_busca}%'))
        
            vendas = query.all()
            return vendas
    except Exception as e:
        logging.error(f"Erro ao buscar vendas pelo termo'{termo_busca}': {e}")
        return []

def get_pagamentos_por_periodo(start_date, end_date, status_pagamento: str = "Todos"):
    try:
        with SessionLocal() as db:
            query = db.query(Pagamento).options(joinedload(Pagamento.fornecedor))
            if start_date and end_date:
                query = query.filter(Pagamento.data_vencimento.between(start_date, end_date))
            elif start_date:
                query = query.filter(Pagamento.data_vencimento >= start_date)
            elif end_date:
                query = query.filter(Pagamento.data_vencimento <= end_date)
            
            if status_pagamento == "Pagas":
                query = query.filter(Pagamento.data_pagamento.is_not(None))
            elif status_pagamento == "Não Pagas":
                query = query.filter(Pagamento.data_pagamento.is_(None))
            pagamentos_periodo = query.all()
            return pagamentos_periodo
    except Exception as e:
        logging.error(f"Erro ao buscar pagamentos pela data '{start_date, end_date}': {e}")
        return []

def get_pagamentos_nao_pagos():
    try:
        with SessionLocal() as db:
            return db.query(Pagamento).options(joinedload(Pagamento.fornecedor)).filter(Pagamento.data_pagamento.is_(None)).order_by(Pagamento.data_vencimento).all()
    except Exception as e:
        logging.error(f"Erro ao buscar pagamentos não pagos: {e}")
        return []
    
def search_pagamentos_nao_pagos(criterio: str, valor: str):
    try:
        with SessionLocal() as db:
            query = db.query(Pagamento).options(joinedload(Pagamento.fornecedor)).filter(Pagamento.data_pagamento.is_(None))
            if criterio == "Fornecedor":
                query = query.join(Fornecedor).filter(Fornecedor.nome_fornecedor.ilike(f'%{valor}%'))
            elif criterio == "Número da nota":
                query = query.filter(Pagamento.numero_nota.ilike(f'%{valor}%'))
            criterio_selecionado = query.order_by(Pagamento.data_vencimento).all()
            return criterio_selecionado
    except Exception as e:
        logging.error(f"Erro ao buscar pagamentos não pagos pelo critério '{criterio}': {e}")
        return []