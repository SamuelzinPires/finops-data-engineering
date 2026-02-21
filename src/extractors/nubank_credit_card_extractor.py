import pandas as pd
import hashlib
from typing import List
import os
from src.database.models import Transaction

class NubankCreditCardExtractor:
    def extract(self, file_path: str) -> List[Transaction]:
        """
        Lê um arquivo CSV de fatura do Cartão Nubank e converte em objetos Transaction.
        Gera um hash_id sintético pois o arquivo não possui ID único.
        
        Regras de Negócio:
        - Layout esperado: date, title, amount
        - Categoria: Fixa como "Cartão de Crédito"
        - Sinal: Valores positivos no CSV viram negativos (Despesa)
        """
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        try:
            # Leitura do CSV
            # O CSV de cartão do Nubank exportado pelo app atual tem: date, title, amount
            df = pd.read_csv(file_path)
            
            # Tratamento de Colunas (Regra de Ouro: Limpar espaços extras)
            # Ex: " title " vira "title"
            df.columns = df.columns.str.strip()
            
            # --- CORRECAO: Remove linha de "Pagamento recebido" ---
            # O CSV do cartao inclui um credito quando a fatura e paga.
            # Esse valor NAO e um gasto — e apenas o registro do pagamento recebido pelo cartao.
            # Se nao remover, ele aparece inflado como gasto no dashboard.
            df = df[~df['title'].str.contains('Pagamento recebido', case=False, na=False)].copy()
            # --- FIM CORRECAO ---
            
            # Validação de Colunas Obrigatórias
            required_columns = ['date', 'title', 'amount']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Colunas faltando no CSV: {missing_columns}. Esperado: {required_columns}")
            
            transactions = []
            
            for _, row in df.iterrows():
                # Tratamento de Data
                try:
                    # Tenta formato YYYY-MM-DD (padrão comum do Pandas/Nubank)
                    date_val = pd.to_datetime(row['date']).date()
                except:
                    # Fallback para formato brasileiro DD/MM/YYYY
                    date_val = pd.to_datetime(row['date'], format='%d/%m/%Y').date()

                # Tratamento de Valor e Inversão de Sinal
                # No CSV do cartão, gastos vêm positivos (ex: 15.90)
                # No banco, gastos devem ser negativos (ex: -15.90)
                amount_raw = float(row['amount'])
                amount_final = amount_raw * -1
                
                # 3. Descrição e Categoria
                description_val = str(row['title'])
                category_val = "Cartão de Crédito" # Categoria fixa pois o CSV não traz mais
                
                # 4. Geração do Hash Sintético (MD5)
                # Usamos os valores ORIGINAIS para garantir que o hash seja sempre o mesmo para a mesma linha
                # String base: "2023-10-05" + "15.9" + "Uber Trip"
                raw_string = f"{row['date']}{row['amount']}{row['title']}"
                
                # Gera o MD5
                hash_id = hashlib.md5(raw_string.encode('utf-8')).hexdigest()
                
                transaction = Transaction(
                    date=date_val,
                    amount=amount_final,
                    description=description_val,
                    category=category_val,
                    source="Nubank Credit Card",
                    hash_id=hash_id
                )
                transactions.append(transaction)
                
            return transactions

        except Exception as e:
            raise ValueError(f"Erro ao processar fatura de cartão {file_path}: {e}")
