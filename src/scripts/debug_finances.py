import pandas as pd
import os
from src.database.connection import engine
from src.main import detect_extractor

def analyze_csvs():
    print("\nOr" + "="*40)
    print("ANÁLISE DE ARQUIVOS CSV (DATA/RAW)")
    print("="*40)
    
    raw_dir = "data/raw"
    if not os.path.exists(raw_dir):
        print(f"❌ Diretório {raw_dir} não encontrado.")
        return

    files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
    
    for f in files:
        path = os.path.join(raw_dir, f)
        print(f"\nArquivo: {f}")
        try:
            # Tenta detectar extrator
            extractor, tipo = detect_extractor(path)
            print(f"   -> Extrator Detectado: {tipo}")
            
            # Lê primeiras linhas
            df = pd.read_csv(path, nrows=3)
            print(f"   -> Colunas: {list(df.columns)}")
            print(f"   -> Exemplo de Valores (Primeira linha):")
            print(df.iloc[0].to_dict())
            
        except Exception as e:
            print(f"   Erro ao analisar: {e}")

def audit_database():
    print("\n" + "="*40)
    print("AUDITORIA DO BANCO DE DADOS")
    print("="*40)
    
    try:
        query = "SELECT * FROM transactions"
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("⚠️ Banco de dados vazio.")
            return

        print(f"Total de Transações: {len(df)}")
        
        # 1. Análise por Fonte (Source)
        print("\n--- Saldo por Fonte (Source) ---")
        summary = df.groupby('source')['amount'].sum().reset_index()
        print(summary)
        
        # 2. Verificação de Sinal do Cartão
        print("\n--- Amostra de 'Nubank Credit Card' (Verificar Sinal) ---")
        cc_trans = df[df['source'] == 'Nubank Credit Card'].head(5)
        if not cc_trans.empty:
            print(cc_trans[['date', 'description', 'amount', 'category']])
        else:
            print("Nenhuma transação de cartão encontrada (com source='Nubank Credit Card').")

        # 3. Busca por 'RDB' ou Investimentos
        print("\n--- Busca por 'RDB' ou '150.00' ---")
        invest = df[
            (df['description'].str.contains('RDB', case=False, na=False)) |
            (df['amount'].abs() == 150.00)
        ]
        if not invest.empty:
            print(invest[['date', 'description', 'amount', 'category', 'source']])
        else:
            print("Nenhuma transação 'RDB' ou valor 150.00 encontrada.")
            
    except Exception as e:
        print(f"Erro ao ler banco de dados: {e}")

if __name__ == "__main__":
    analyze_csvs()
    audit_database()
