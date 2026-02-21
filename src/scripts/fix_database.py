from src.database.connection import SessionLocal
from src.transformers.category_transformer import CategoryTransformer
from src.database.models import Transaction

def fix_categories():
    print("Iniciando correcao de categorias no Banco de Dados...")
    db = SessionLocal()
    transformer = CategoryTransformer()
    
    try:
        transactions = db.query(Transaction).all()
        
        print(f"Processando {len(transactions)} transacoes...")
        
        updated_count = 0
        for transaction in transactions:
            old_category = transaction.category
            
            # Re-aplica a transformação
            transformer.transform_transaction(transaction)
            
            if transaction.category != old_category:
                updated_count += 1
                # print(f"  Atualizado: {transaction.description} | {old_category} -> {transaction.category}")
        
        db.commit()
        print(f"Correcao concluida! {updated_count} transacoes atualizadas.")
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao corrigir banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_categories()
