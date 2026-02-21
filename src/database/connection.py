import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Carrega as variáveis do arquivo .env
load_dotenv()

# Busca as configurações nas variáveis de ambiente
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Monta a URL de conexão do PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criando a ENGINE (O Motor)
# A engine é a fábrica de conexões. Ela sabe onde o banco está e como falar com ele.
# echo=False: Se True, imprime todo SQL executado no terminal (bom para debug).
engine = create_engine(DATABASE_URL, echo=False)

# Criando a SESSIONLOCAL (A Fábrica de Sessões)
# Uma "Sessão" é um espaço de trabalho temporário. É como abrir uma aba no navegador.
# autocommit=False: controlar quando salvar (commit).
# autoflush=False: controlar quando enviar para o banco.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para pegar uma sessão do banco (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Sempre fecha a sessão ao terminar!

# Teste de Conexão (Só roda se executar este arquivo direto)
if __name__ == "__main__":
    try:
        # Tenta conectar e executar um comando simples
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 'Conexão Funcionou! O Banco está Vivo!'"))
            print("\n✅ SUCESSO:")
            print(result.scalar())
            print(f"Conectado em: {DB_HOST}:{DB_PORT}/{DB_NAME}\n")
    except Exception as e:
        print("\n❌ ERRO NA CONEXÃO:")
        print(e)
        print("\nDica: Verifique se o Docker está rodando e se as credenciais no .env estão corretas.\n")
