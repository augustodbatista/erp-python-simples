from models import Pagamento
from database import SessionLocal

def add_pagamento(dados_pagamento: dict):
    
    novo_pagamento = Pagamento(
        numero_nota=dados_pagamento['numero_nota'],
        data_vencimento=dados_pagamento['data_vencimento'],
        valor_nota=dados_pagamento['valor_nota'],
        data_pagamento=dados_pagamento.get('data_pagamento'), # .get() é mais seguro para campos opcionais
        fornecedor_id=dados_pagamento['fornecedor_id']
    )

    try:
        with SessionLocal() as db:
            db.add(novo_pagamento)
            db.commit()
            db.refresh(novo_pagamento)
            return novo_pagamento
    except Exception as e:
        return None