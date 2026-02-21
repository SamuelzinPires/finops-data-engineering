from typing import List
from src.database.models import Transaction

class CategoryTransformer:
    def __init__(self):
        # Dicionário de Regras (Categorias -> Palavras-Chave)
        self.categories_map = {
            'Pagamento de Fatura': [
                'pagamento de fatura', 'fatura cartao', 'pagamento recebido', 'pagamento de fatura'
            ],
            'Investimento': [
                'nu invest', 'nuinvest', 'easynvest', 'rico', 'xp', 'clear', 'binance', 'cripto', 'poupanca', 'tesouro', 'cdb', 'aplicacao rdb', 'aplicacao', 'rdb', 'caixinha', 'nubank reserva'
            ],
            'Transferência Interna': [
                'resgate', 'transferencia entre contas'
            ],
            'Casa': [
                'aluguel', 'condominio', 'energia eletrica', 'cemig', 'copasa',
                'claro residencial', 'vivo fibra', 'agua', 'gas encanado'
            ],
            'Assinaturas': [
                'assinatura', 'recorrente', 'timsa', 'tim s a', '02.421.421', 'vivo', 'claro', 'telefone', 'celular', 'google storage', 'icloud'
            ],
            'Delivery': [
                'ifood', 'rappi', 'uber eats', '99food', 'ze delivery', 'delivery'
            ],
            'Transporte': [
                'uber', '99app', '99 - nupay', 'taxi', 'gasolina', 'posto de combustivel',
                'ipva', 'estacionamento', 'onibus', 'metro', 'mobilidade'
            ],
            'Supermercado': [
                'supermercado', 'mercado', 'atacadao', 'pao de acucar', 'assai',
                'padaria', 'mercearia', 'emporio', 'bebidas geladas', 'carrefour', 'extra'
            ],
            'Farmacia': [
                'farmacia', 'drogaria', 'drogamarys', 'droga star', 'pacheco', 'raia',
                'remedio', 'droga'
            ],
            'Saude': [
                'medico', 'hospital', 'laboratorio', 'consulta', 'exame',
                'clinica', 'psicologo', 'dentista', 'saude'
            ],
            'Lazer': [
                'cinema', 'netflix', 'spotify', 'prime video', 'disney', 'restaurante',
                'show', 'gaming', 'steam', 'playstation', 'xbox', 'sevenx', 'butequim'
            ],
            'Roupa': [
                'zara', 'renner', 'nike', 'adidas', 'americanas', 'daiso', 'kalunga',
                'shein', 'shopee', 'centauro', 'c&a', 'cea'
            ],
            'Educacao': [
                'faculdade', 'universidade', 'curso', 'mensalidade escolar',
                'escola', 'udemy', 'alura', 'hotmart', 'saraiva'
            ],
            'Beleza': [
                'salao', 'manicure', 'barbeiro', 'estetica', 'sobrancelha'
            ],
            'Presentes': [
                'presente', 'gift', 'brinquedo', 'la belle'
            ],
            'Taxas': [
                'tarifa bancaria', 'iof', 'juros', 'multa', 'anuidade'
            ],
            'Emprestimo': [
                'emprestimo', 'financiamento', 'parcela'
            ],
        }

    def transform_transaction(self, transaction: Transaction) -> Transaction:
        """
        Aplica regras de categorização em uma única transação.
        """
        import re
        description_lower = transaction.description.lower()
        
        for category, keywords in self.categories_map.items():
            for keyword in keywords:
                # Para keywords curtas (3 chars ou menos), busca palavra exata
                if len(keyword) <= 3:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    if re.search(pattern, description_lower):
                        transaction.category = category
                        return transaction
                else:
                    if keyword in description_lower:
                        transaction.category = category
                        return transaction
        
        return transaction

    def transform_list(self, transactions: List[Transaction]) -> List[Transaction]:
        """
        Aplica a transformação em uma lista de transações.
        """
        updated_transactions = []
        for transaction in transactions:
            updated_transaction = self.transform_transaction(transaction)
            updated_transactions.append(updated_transaction)
            
        return updated_transactions
