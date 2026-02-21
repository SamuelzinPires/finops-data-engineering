from sqlalchemy import create_engine, text

# Configuração da conexão (igual ao seu docker-compose.yaml)
# Usuario: admin
# Senha: admin
# Host: localhost
# Porta: 5432
# Banco: financas_pessoais
DATABASE_URL = "postgresql://admin:admin@localhost:5432/financas_pessoais"

def testar_conexao():
    try:
        # Cria a engine (o motor de conexão)
        engine = create_engine(DATABASE_URL)
        
        # Tenta conectar e executar um comando simples
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 'Conexão Funcionou! O Banco está Vivo!'"))
            print("✅ SUCESSO:")
            print(result.scalar())
            
    except Exception as e:
        print("❌ ERRO NA CONEXÃO:")
        print(e)

if __name__ == "__main__":
    testar_conexao()