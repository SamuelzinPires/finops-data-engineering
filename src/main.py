from src.database.connection import SessionLocal, get_db
from src.extractors.nubank_extractor import NubankExtractor
from src.extractors.nubank_credit_card_extractor import NubankCreditCardExtractor
from src.repositories.transaction_repository import TransactionRepository
from src.transformers.category_transformer import CategoryTransformer
import os
import sys
import pandas as pd

def detect_extractor(file_path: str):
    """
    Analisa a primeira linha do CSV e decide qual extrator usar.
    """
    try:
        # Lê apenas o cabeçalho para ser rápido
        df_head = pd.read_csv(file_path, nrows=1)
        columns = [col.lower().strip() for col in df_head.columns]
        
        # Lógica de Decisão
        # Se tiver 'identificador' -> É NuConta
        if 'identificador' in columns:
            return NubankExtractor(), "NuConta"
        
        # Se tiver 'title' mas NÃO 'identificador' -> É Cartão
        if 'title' in columns:
            return NubankCreditCardExtractor(), "Cartão de Crédito"
            
        raise ValueError("Formato desconhecido: As colunas não batem com nenhum extrator conhecido.")
        
    except Exception as e:
        raise ValueError(f"Erro ao detectar formato do arquivo: {e}")

def run_pipeline(file_path: str):
    """
    Executa o pipeline completo de importação de dados.
    1. Extração
    2. Transformação (Categorização)
    3. Carga (Banco de Dados)
    """
    
    print(f"[INFO] Iniciando Pipeline para o arquivo: {file_path}")
    
    # Passo 1: Detecção e Extração
    try:
        extractor, tipo_arquivo = detect_extractor(file_path)
        print(f"[INFO] Tipo de arquivo detectado: {tipo_arquivo}")
        
        print("[INFO] Lendo arquivo CSV...")
        transactions = extractor.extract(file_path)
        print(f"[OK] Arquivo lido com sucesso! {len(transactions)} transações encontradas.")
    except Exception as e:
        print(f"[ERROR] Erro na extração: {e}")
        return

    # Passo 2: Transformação (Categorização)
    try:
        print("[INFO] Aplicando regras de categorização...")
        transformer = CategoryTransformer()
        transactions = transformer.transform_list(transactions)
        print("[OK] Categorias aplicadas com sucesso!")
    except Exception as e:
        print(f"[ERROR] Erro na transformação: {e}")
        return

    # Passo 3: Banco de Dados
    db = SessionLocal()
    
    try:
        # Passo 4: Repositório
        repo = TransactionRepository(db)
        
        imported_count = 0
        ignored_count = 0
        
        print("[INFO] Iniciando gravação no banco de dados...")
        
        # Passo 5: Loop de Carga
        for transaction in transactions:
            # Verifica se já existe pelo hash
            if repo.exists_by_hash(transaction.hash_id):
                ignored_count += 1
                # print(f"  -> Ignorado (duplicado): {transaction.description}")
            else:
                repo.save(transaction)
                imported_count += 1
                # print(f"  -> Salvo: {transaction.description}")
        
        # Resumo
        print("\n" + "="*40)
        print("PROCESSO FINALIZADO!")
        print("="*40)
        print(f"-> Total Importado: {imported_count}")
        print(f"-> Total Ignorado: {ignored_count}")
        print("="*40)
        
    except Exception as e:
        print(f"[ERROR] Erro durante a gravação no banco: {e}")
    finally:
        db.close()
        print("[INFO] Conexão com o banco fechada.")

if __name__ == "__main__":
    # Caminho do arquivo CSV
    if len(sys.argv) > 1:
        FILE_PATH = sys.argv[1]
    else:
        # Padrão: Ajuste conforme o nome do seu arquivo real
        FILE_PATH = "data/raw/NU_Jan-Completo.csv"
    
    # Verifica se o arquivo existe antes de rodar
    if not os.path.exists(FILE_PATH):
        print(f"[WARNING] Arquivo não encontrado: {FILE_PATH}")
        print("Dica: Ajuste a variável FILE_PATH no final do arquivo src/main.py")
        print("Ou rode: python src/main.py caminha/do/seu/arquivo.csv")
    else:
        run_pipeline(FILE_PATH)
