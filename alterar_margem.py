import os
import libsql
from dotenv import load_dotenv

load_dotenv()

print("Conectando ao Turso...")

db = libsql.connect(
    os.getenv("TURSO_DATABASE_URL"),
    auth_token=os.getenv("TURSO_AUTH_TOKEN")
)

cursor = db.cursor()

try:
    cursor.execute("""
        ALTER TABLE usuarios
        ADD COLUMN margem_padrao INTEGER DEFAULT 25
    """)
    db.commit()
    print("✅ Coluna criada com sucesso!")

except Exception as e:
    print("ℹ️", e)

cursor.execute("PRAGMA table_info(usuarios)")

print("\nColunas da tabela usuarios:")

for coluna in cursor.fetchall():
    print("-", coluna[1])

db.close()