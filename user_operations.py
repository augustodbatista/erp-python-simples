from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Usuario
from passlib.context import CryptContext

DATABASE_URL = "sqlite:///erp_database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def add_user(nome_usuario, senha, cargo):
    senha_hash = pwd_context.hash(senha)

    db = SessionLocal()
    
    novo_usuario = Usuario(
        nome_usuario=nome_usuario,
        senha_hash=senha_hash,
        cargo=cargo
    )
    
    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        print(f"Usuário '{novo_usuario.nome_usuario}' criado com sucesso com o id {novo_usuario.id}!")
        return novo_usuario
    except Exception as e:
        print(f"Erro ao adicionar usuário: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def verify_user(nome_usuario, senha):
    db = SessionLocal()
    try:
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
    finally:
        db.close()
        
if __name__ == "__main__":
    print("Iniciando o processo de adição de usuário...")
    add_user("admin", "senha123", "Administrador")
    print("Processo concluído.")