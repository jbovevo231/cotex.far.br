from database.connection import get_db

db = get_db()

usuarios = db.execute("""
SELECT id, nome, cnpj, email
FROM usuarios
""").fetchall()

print(f"Total de usuários: {len(usuarios)}")

for usuario in usuarios:
    print(dict(usuario))