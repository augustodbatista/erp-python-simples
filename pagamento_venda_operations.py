import logging
from database import SessionLocal
from models import PagamentoVenda

def add_pagamento_venda(dados_pagamento: dict):
    
    novo_pagamento = PagamentoVenda(
        valor_pago=dados_pagamento['valor_pago'],
        data_pagamento=dados_pagamento['data_pagamento'],
        forma_pagamento=dados_pagamento.get('forma_pagamento'),
        venda_id=dados_pagamento['venda_id']
    )

    try:
        with SessionLocal() as db:
            db.add(novo_pagamento)
            db.commit()
            db.refresh(novo_pagamento)
            logging.info(f"Pagamento de {novo_pagamento.valor_pago} para a venda ID {novo_pagamento.venda_id} adicionado com sucesso.")
            return novo_pagamento
    except Exception as e:
        logging.error(f"Erro ao adicionar pagamento para a venda ID {dados_pagamento['venda_id']}: {e}")
        return None