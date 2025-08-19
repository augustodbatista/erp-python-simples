from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Vendedor, Cliente, Fornecedor, Pagamento, Venda

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_todos_vendedores():
    db = SessionLocal()
    try:
        vendedores = db.query(Vendedor).all()
        return vendedores
    finally:
        db.close()

def get_todos_clientes():
    db = SessionLocal()
    try:
        clientes = db.query(Cliente).all()
        return clientes
    finally:
        db.close()

def search_clientes_por_nome(termo_busca: str):
    db = SessionLocal()
    try:
        search_clientes = db.query(Cliente).filter(Cliente.nome_cliente.ilike(f'%{termo_busca}%')).all()
        return search_clientes
    finally:
        db.close()

def search_fornecedores_por_nome(termo_busca: str):
    db = SessionLocal()
    try:
        search_fornecedores = db.query(Fornecedor).filter(Fornecedor.nome_fornecedor.ilike(f'%{termo_busca}%')).all()
        return search_fornecedores
    finally:
        db.close()


def search_vendas_nao_pagas(termo_busca: str):
    db = SessionLocal()
    try:
        # Import Venda and Cliente inside the function to avoid circular imports if models.py imports data_operations
        from models import Venda, Cliente
        
        query = db.query(Venda).options(joinedload(Venda.cliente)).filter(Venda.pago == False)

        if termo_busca.isdigit(): # Assume it's a notinha number if it's all digits
            query = query.filter(Venda.numero_notinha == int(termo_busca))
        else: # Assume it's a client name
            query = query.join(Cliente).filter(Cliente.nome_cliente.ilike(f'%{termo_busca}%'))
        
        vendas = query.all()
        return vendas
    finally:
        db.close()

