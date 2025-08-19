from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Pagamento

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_pagamento(dados_pagamento: dict):

    db = SessionLocal()
    
    novo_pagamento = Pagamento(
        numero_nota=dados_pagamento['numero_nota'],
        data_vencimento=dados_pagamento['data_vencimento'],
        valor_nota=dados_pagamento['valor_nota'],
        data_pagamento=dados_pagamento.get('data_pagamento'), # .get() é mais seguro para campos opcionais
        fornecedor_id=dados_pagamento['fornecedor_id']
    )

    try:
        db.add(novo_pagamento)
        db.commit()
        db.refresh(novo_pagamento)
        print(f"Pagamento ID {novo_pagamento.id} adicionada com sucesso!")
        return novo_pagamento
    except Exception as e:
        print(f"Erro ao adicionar pagamento: {e}")
        db.rollback()
        return None
    finally:
        db.close()