from sqlalchemy.orm import Session
from src.database.models import Transaction

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, transaction: Transaction) -> Transaction:
        """
        Salva uma transação no banco de dados.
        """
        try:
            # Adiciona o objeto à sessão (prepara para salvar)
            self.db.add(transaction)
            
            # Efetiva a gravação no banco de dados
            # Se não der commit, nada é salvo de verdade!
            self.db.commit()
            
            # Atualiza o objeto com dados do banco (ex: pega o ID gerado)
            # Sem isso, o objeto 'transaction' ficaria sem o ID até a gente buscar de novo.
            self.db.refresh(transaction)
            
            return transaction
        except Exception as e:
            # Se der erro, desfaz qualquer alteração pendente para não travar o banco
            self.db.rollback()
            raise e

    def exists_by_hash(self, hash_id: str) -> bool:
        """
        Verifica se já existe uma transação com este hash_id.
        Retorna True se existir, False se não.
        """
        # Faz uma consulta (SELECT) contando quantos registros têm esse hash
        # O uso de .first() é eficiente pois para na primeira ocorrência
        existing_transaction = self.db.query(Transaction).filter(Transaction.hash_id == hash_id).first()
        
        return existing_transaction is not None
