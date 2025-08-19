from sqlalchemy.orm import joinedload
from models import Venda, Pagamento, Cliente, Vendedor
from sqlalchemy import func
from datetime import date
from database import SessionLocal
import logging

def add_venda(dados_venda: dict):
  
    nova_venda = Venda(
        data_venda=dados_venda['data_venda'],
        numero_notinha=dados_venda['numero_notinha'],
        valor_total=dados_venda['valor_total'],
        pago=dados_venda['pago'],
        forma_pagamento=dados_venda['forma_pagamento'],
        data_vencimento=dados_venda.get('data_vencimento'), # .get() é mais seguro para campos opcionais
        cliente_id=dados_venda['cliente_id'],
        vendedor_id=dados_venda['vendedor_id'],
        participacao_vendas=dados_venda['participacao_vendas']
    )

    try:
        with SessionLocal() as db:
            db.add(nova_venda)
            db.commit()
            db.refresh(nova_venda)
            logging.info(f"Venda'{dados_venda['numero_notinha']}' (ID: {nova_venda.id}) adicionado com sucesso.")
            return nova_venda
    except Exception as e:
        logging.error(f"Erro ao adicionar venda '{dados_venda['numero_notinha']}': {e}")
        return None

def get_vendas_nao_pagas():

    try:
        with SessionLocal() as db:
            vendas_nao_pagas = db.query(Venda).filter(Venda.pago == False).order_by(Venda.data_vencimento).all()
            return vendas_nao_pagas
    except Exception as e:
        logging.error(f"Erro ao buscar todas vendas nao pagas: {e}")
        return []

def marcar_venda_como_paga(venda_id: int):

    try:
        with SessionLocal() as db:

            venda = db.query(Venda).filter(Venda.id == venda_id).first()
            if venda:
                venda.pago = True
                db.commit()
                db.refresh(venda)
                logging.info(f"Venda {venda_id} marcada como paga.")
                return venda
            else:
                logging.warning(f"Venda {venda_id} não foi marcada como paga.")
                return None
    except Exception as e:
        logging.error(f"Erro ao marcar venda {venda_id} como paga no banco de dados: {e}")
        return None



def get_sales_by_period_and_vendedor(start_date: date, end_date: date, vendedor_id: int = None):

    try:
        with SessionLocal() as db:
            query = db.query(Venda).options(joinedload(Venda.cliente), joinedload(Venda.vendedor)).filter(Venda.data_venda.between(start_date, end_date))
            if vendedor_id:
                query = query.filter(Venda.vendedor_id == vendedor_id)
            return query.all()
    except Exception as e:
        logging.error(f"Erro ao buscar vendas por período e vendedor: {e}")
        return []

def get_sales_by_period_and_cliente(start_date: date, end_date: date, cliente_id: int = None):

    try:
        with SessionLocal() as db:
            query = db.query(Venda).options(joinedload(Venda.cliente), joinedload(Venda.vendedor)).filter(Venda.data_venda.between(start_date, end_date))
            if cliente_id:
                query = query.filter(Venda.cliente_id == cliente_id)
            return query.all()
    except Exception as e:
        logging.error(f"Erro ao buscar vendas por período e cliente: {e}")
        return []

def get_total_sales_by_period(start_date: date, end_date: date):

    try:
        with SessionLocal() as db:
            total_sales = db.query(func.sum(Venda.valor_total)).filter(Venda.data_venda.between(start_date, end_date)).scalar()
            return total_sales if total_sales is not None else 0.0
    except Exception as e:
        logging.error(f"Erro ao buscar vendas por período {start_date, end_date}: {e}")
        return None

def get_paid_unpaid_sales_by_client(cliente_id: int, paid_status: bool = None):

    try:
        with SessionLocal() as db:
            query = db.query(Venda).options(joinedload(Venda.cliente), joinedload(Venda.vendedor)).filter(Venda.cliente_id == cliente_id)
            if paid_status is not None:
                query = query.filter(Venda.pago == paid_status)
            return query.all()
    except Exception as e:
        logging.error(f"Erro ao buscar vendas: {e}")
        return []