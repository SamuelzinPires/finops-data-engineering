from src.database.connection import engine
from sqlalchemy import text

def truncate_db():
    print("Truncating transactions table...")
    with engine.connect() as con:
        con.execute(text("TRUNCATE TABLE transactions;"))
        con.commit()
    print("Truncate complete.")

if __name__ == "__main__":
    truncate_db()
