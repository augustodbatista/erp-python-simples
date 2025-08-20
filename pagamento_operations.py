from models import Pagamento
from database import SessionLocal
import logging

def add_pagamento(dados_pagamento: dict):
    
    novo_pagamento = Pagamento(
        numero_nota=dados_pagamento['numero_nota'],
        data_vencimento=dados_pagamento['data_vencimento'],
        valor_nota=dados_pagamento['valor_nota'],
        data_pagamento=dados_pagamento.get('data_pagamento'),
        forma_pagamento=dados_pagamento.get('forma_pagamento'),
        fornecedor_id=dados_pagamento['fornecedor_id']
    )

    try:
        with SessionLocal() as db:
            db.add(novo_pagamento)
            db.commit()
            db.refresh(novo_pagamento)
            logging.info(f"Pagamento '{novo_pagamento.numero_nota}' (ID: {novo_pagamento.id}) adicionado com sucesso.")
            return novo_pagamento
    except Exception as e:
        logging.error(f"Erro ao adicionar pagamento '{dados_pagamento['numero_nota']}': {e}")
        return None
    
def atualizar_pagamento(pagamento_id: int, novos_dados: dict):
    try:
        with SessionLocal() as db:
            pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
            if pagamento:
                pagamento.data_pagamento = novos_dados.get('data_pagamento')
                pagamento.forma_pagamento = novos_dados.get('forma_pagamento')
                db.commit()
                db.refresh(pagamento)
                logging.info(f"Pagamento {pagamento_id} marcada como paga.")
                return pagamento
            else:
                logging.warning(f"Pagamento {pagamento_id} não foi marcada como paga.")
                return None
    except Exception as e:
        logging.error(f"Erro ao marcar pagamento {pagamento_id} como paga no banco de dados: {e}")
        return None