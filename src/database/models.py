from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from src.database.connection import engine

# Cria a classe Base do SQLAlchemy
# Todas as nossas tabelas vão herdar dessa classe
Base = declarative_base()

class Transaction(Base):
    """
    Representa a tabela 'transactions' no banco de dados.
    """
    __tablename__ = 'transactions'

    # Colunas Obrigatórias
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)     # Valor da transação
    description = Column(String, nullable=False) # Nome da loja/pix
    category = Column(String, nullable=True)   # Ex: "Mercado", "Lazer"
    source = Column(String, nullable=True)     # Ex: "Nubank", "Inter"
    
    # (Segurança e Idempotência)
    # hash_id é um código único gerado para cada transação (ex: MD5 da data+valor+descrição).
    # unique=True: O banco de dados BLOQUEIA se tentarmos inserir o mesmo hash duas vezes.
    # index=True: Cria um índice para busca rápida, ideal para verificar existência antes de inserir.
    hash_id = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"<Transaction(date={self.date}, desc={self.description}, amount={self.amount})>"

# Bloco de Execução Principal
if __name__ == "__main__":
    print("🔨 Iniciando criação de tabelas no banco de dados...")
    try:
        # Cria todas as tabelas definidas que herdam de Base (no caso, 'transactions')
        # Se a tabela já existir, ele NÃO faz nada (não apaga dados).
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'transactions' verificada/criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
