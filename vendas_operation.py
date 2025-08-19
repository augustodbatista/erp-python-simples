from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from models import Venda, Pagamento, Cliente, Vendedor
from sqlalchemy import func
from datetime import date

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_venda(dados_venda: dict):

    db = SessionLocal()
    
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

def get_vendas_nao_pagas():

    db = SessionLocal()

    try:
        vendas_nao_pagas = db.query(Venda).filter(Venda.pago == False).order_by(Venda.data_vencimento).all()
        return vendas_nao_pagas
    finally:
        db.close()

def marcar_venda_como_paga(venda_id: int):
    db = SessionLocal()
    try:
        venda = db.query(Venda).filter(Venda.id == venda_id).first()
        if venda:
            venda.pago = True
            db.commit()
            db.refresh(venda)
            print(f"Venda ID {venda.id} marcada como paga.")
            return venda
        else:
            print(f"Venda ID {venda_id} não encontrada.")
            return None
    except Exception as e:
        print(f"Erro ao atualizar venda: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def get_sales_by_period_and_vendedor(start_date: date, end_date: date, vendedor_id: int = None):
    db = SessionLocal()
    try:
        query = db.query(Venda).options(joinedload(Venda.cliente), joinedload(Venda.vendedor)).filter(Venda.data_venda.between(start_date, end_date))
        if vendedor_id:
            query = query.filter(Venda.vendedor_id == vendedor_id)
        return query.all()
    finally:
        db.close()

def get_sales_by_period_and_cliente(start_date: date, end_date: date, cliente_id: int = None):
    db = SessionLocal()
    try:
        query = db.query(Venda).options(joinedload(Venda.cliente), joinedload(Venda.vendedor)).filter(Venda.data_venda.between(start_date, end_date))
        if cliente_id:
            query = query.filter(Venda.cliente_id == cliente_id)
        return query.all()
    finally:
        db.close()

def get_total_sales_by_period(start_date: date, end_date: date):
    db = SessionLocal()
    try:
        total_sales = db.query(func.sum(Venda.valor_total)).filter(Venda.data_venda.between(start_date, end_date)).scalar()
        return total_sales if total_sales is not None else 0.0
    finally:
        db.close()

def get_paid_unpaid_sales_by_client(cliente_id: int, paid_status: bool = None):
    db = SessionLocal()
    try:
        query = db.query(Venda).options(joinedload(Venda.cliente), joinedload(Venda.vendedor)).filter(Venda.cliente_id == cliente_id)
        if paid_status is not None:
            query = query.filter(Venda.pago == paid_status)
        return query.all()
    finally:
        db.close()