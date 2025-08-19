from models import Usuario
from passlib.context import CryptContext
from database import SessionLocal
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def add_user(nome_usuario, senha, cargo):
    senha_hash = pwd_context.hash(senha)
    
    novo_usuario = Usuario(
        nome_usuario=nome_usuario,
        senha_hash=senha_hash,
        cargo=cargo
    )
    
    try:
        with SessionLocal() as db:
            db.add(novo_usuario)
            db.commit()
            db.refresh(novo_usuario)
            logging.info(f"Usuário '{novo_usuario.nome_usuario}' (ID: {novo_usuario.id}) adicionado com sucesso.")
            return novo_usuario
    except Exception as e:
        logging.error(f"Erro ao tentar cadastrar o usuário '{nome_usuario}': {e}")
        return None

def verify_user(nome_usuario, senha):

    try:
        with SessionLocal() as db:
        
            usuario = db.query(Usuario).filter(Usuario.nome_usuario == nome_usuario).first()
            if usuario is None:
                logging.warning(f"Tentativa de login falhou: usuário '{nome_usuario}' não encontrado.")
                return None
            else:
                senha_valida = pwd_context.verify(senha, usuario.senha_hash)
                if senha_valida:
                    logging.info(f"Usuário '{usuario.nome_usuario}' autenticado com sucesso!")
                    return usuario
                else:
                    logging.warning(f"Tentativa de login falhou para o usuário '{nome_usuario}': senha incorreta.")
                    return None
    except Exception as e:
        logging.error(f"Erro no banco de dados ao tentar verificar o usuário '{nome_usuario}': {e}")
        return None
        
if __name__ == "__main__":
    print("Iniciando o processo de adição de usuário...")
    add_user("admin", "senha123", "Administrador")
    print("Processo concluído.")