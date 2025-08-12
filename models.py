from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Vendedor(Base):
    __tablename__ = 'vendedores'

    id = Column(Integer, primary_key=True) 
    nome_vendedor = Column(String(100), nullable=False, unique=True)
    data_contratacao = Column(Date, nullable=False)
    vendas = relationship("Venda", back_populates="vendedor")

    def __repr__(self):
        return f"Vendedor(id={self.id}, nome='{self.nome_vendedor}')"
    
class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome_cliente = Column(String(100), nullable=False)
    endereco = Column(String(200))
    telefone = Column(String(20))
    vendas = relationship("Venda", back_populates="cliente")

    def __repr__(self):
        return f"Cliente(id={self.id}, nome='{self.nome_cliente}')"

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome_usuario = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(128), nullable=False)
    cargo = Column(String(50), nullable=False)

    def __repr__(self):
        return f"Usuario(id={self.id}, nome='{self.nome_usuario}', cargo='{self.cargo}')" 
    
class Venda(Base):
    __tablename__ = 'vendas'

    id = Column(Integer, primary_key=True)
    numero_notinha = Column(Integer, nullable=False)
    data_venda = Column(Date, nullable=False)
    valor_total = Column(Numeric(10,2), nullable=False)
    pago = Column(Boolean, nullable=False, default=False)
    forma_pagamento = Column(String(50), nullable=False)
    data_vencimento = Column(Date)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    vendedor_id = Column(Integer, ForeignKey('vendedores.id'), nullable=False)
    participacao_vendas = Column(Boolean, default=False)
    cliente = relationship("Cliente", back_populates="vendas")
    vendedor = relationship("Vendedor", back_populates="vendas")
    def __repr__(self):
        return f"Venda(id={self.id}, cliente_id={self.cliente_id}, vendedor_id={self.vendedor_id}, valor_total={self.valor_total})"
    
class Fornecedor(Base):
    __tablename__ = 'fornecedores'

    id = Column(Integer, primary_key=True)
    nome_fornecedor = Column(String(50), nullable=False)
    cpf_cnpj = Column(String(50))
    telefone = Column(String(50))
    endereco = Column(String(50))
    pagamentos = relationship("Pagamento", back_populates="fornecedor")
    def __repr__(self):
        return f"Fornecedor(id={self.id}, nome_fornecedor={self.nome_fornecedor})"

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True)
    numero_nota = Column(String(50))
    data_vencimento = Column(Date, nullable=False)
    valor_nota = Column(Numeric(10,2), nullable=False)
    data_pagamento = Column(Date)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'), nullable=False)
    fornecedor = relationship("Fornecedor", back_populates="pagamentos")
    def __repr__(self):
        return f"Pagamento(id={self.id}, numero_nota={self.numero_nota}, data_vencimento={self.data_vencimento}, valor_nota={self.valor_nota})"