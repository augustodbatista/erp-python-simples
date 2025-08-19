from models import Usuario
from passlib.context import CryptContext
from database import SessionLocal

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
            return novo_usuario
    except Exception as e:
        return None

def verify_user(nome_usuario, senha):

    try:
        with SessionLocal() as db:
        
            usuario = db.query(Usuario).filter(Usuario.nome_usuario == nome_usuario).first()
            if usuario is None:
                print("Usuário não encontrado.")
                return None
            else:
                senha_valida = pwd_context.verify(senha, usuario.senha_hash)
                if senha_valida:
                    print(f"Usuário '{usuario.nome_usuario}' autenticado com sucesso!")
                    return usuario
                else:
                    print("Senha incorreta.")
                    return None
    except Exception as e:
        return None
        
if __name__ == "__main__":
    print("Iniciando o processo de adição de usuário...")
    add_user("admin", "senha123", "Administrador")
    print("Processo concluído.")