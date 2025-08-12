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