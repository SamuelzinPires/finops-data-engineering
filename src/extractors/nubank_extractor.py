import pandas as pd
from typing import List
from datetime import datetime
import os
from src.database.models import Transaction

class NubankExtractor:
    def extract(self, file_path: str) -> List[Transaction]:
        """
        Lê um arquivo CSV do Nubank e converte em uma lista de objetos Transaction.
        """
        
        # Verificação básica de existência do arquivo
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        try:
            # Leitura do CSV
            # O Nubank usa vírgula como separador no padrão global, mas às vezes ponto e vírgula no BR.
            # tentar ler com pandas. O encoding 'latin-1' ou 'utf-8' costuma funcionar.
            df = pd.read_csv(file_path)
            
            # Se a leitura falhar (ex: colunas erradas), o pandas pode lançar erro ou ler errado.
            # Vamos garantir que as colunas essenciais existam.
            required_columns = ['Data', 'Valor', 'Descrição', 'Identificador']
            # Normaliza nomes das colunas para minúsculo para facilitar verificação se necessário, 
            # mas vamos confiar no padrão do Nubank por enquanto ou ajustar se der erro.
            
            # Renomeando para o nosso padrão
            # 'Data' -> 'date'
            # 'Valor' -> 'amount'
            # 'Descrição' -> 'description'
            # 'Identificador' -> 'hash_id'
            column_mapping = {
                'Data': 'date',
                'Valor': 'amount',
                'Descrição': 'description',
                'Identificador': 'hash_id'
            }
            
            # Verifica se as colunas existem antes de renomear
            for col in required_columns:
                if col not in df.columns:
                     # Tenta verificar se é um CSV antigo sem Identificador ou com nomes diferentes
                     # Por enquanto, lançamos erro se não seguir o padrão esperado.
                     raise ValueError(f"Coluna obrigatória não encontrada no CSV: {col}")

            df.rename(columns=column_mapping, inplace=True)

            # Limpeza e Transformação
            
            # ----------------------------------------------------------------------
            # LIMPEZA DE DADOS
            # ----------------------------------------------------------------------
            # Filtrar linhas vazias ou com valor duplicado no CSV (se houver, mas o hash cuida disso no banco)
            # Vamos remover onde amount é nulo
            df.dropna(subset=['amount', 'date'], inplace=True)

            # --- CORRECAO: Remove pares de estorno que se anulam ---
            # O Nubank exporta pares com mesmo Identificador quando um Pix falha e e estornado.
            # Esses pares somam zero e nao representam movimentacao real de dinheiro.
            id_somas = df.groupby('hash_id')['amount'].sum()
            ids_nulos = id_somas[id_somas.abs() < 0.01].index
            df_antes = len(df)
            df = df[~df['hash_id'].isin(ids_nulos)].copy()
            if len(df) < df_antes:
                print(f"  -> {df_antes - len(df)} transacoes de estorno ignoradas (soma zero)")
            # --- FIM CORRECAO ---
            
            # Adiciona a coluna 'source' fixa
            df['source'] = 'Nubank'
            
            # Tratamento de Datas
            # O Nubank geralmente manda DD/MM/YYYY
            # converter para objeto date do Python (YYYY-MM-DD)
            try:
                df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.date
            except Exception as e:
                # Tenta formato alternativo ISO se falhar o BR
                 df['date'] = pd.to_datetime(df['date']).dt.date

            # Converter para lista de objetos Transaction
            transactions = []
            for _, row in df.iterrows():
                # Validação extra de valor
                if row['amount'] == 0:
                    continue # Pula transações de valor zero, se existirem e não forem relevantes

                transaction = Transaction(
                    date=row['date'],
                    amount=float(row['amount']),
                    description=row['description'],
                    source=row['source'],
                    hash_id=str(row['hash_id']) # Garante que seja string
                    # category vamos deixar nulo por enquanto, pois o CSV do Nubank vem sem categoria útil na maioria das vezes,
                    # ou a coluna Categoria do CSV pode ser mapeada se existir. 
                    # O prompt não pediu explicitamente para ler a categoria do CSV, mas se tiver, podemos adicionar.
                    # Vou assumir que o CSV tem a coluna Categoria se o usuário exportou completo, 
                    # mas o mapeamento básico solicitado foi Data, Valor, Descrição, Identificador.
                )
                transactions.append(transaction)
            
            return transactions

        except Exception as e:
            raise ValueError(f"Erro ao processar o arquivo {file_path}: {e}")
