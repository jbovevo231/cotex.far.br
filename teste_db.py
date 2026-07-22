from database.connection import get_db

db = get_db()

print("===== COTACOES =====")
for c in db.execute("PRAGMA table_info(cotacoes)").fetchall():
    print(c)

print("\n===== COTACAO_ITENS =====")
for c in db.execute("PRAGMA table_info(cotacao_itens)").fetchall():
    print(c)

print("\n===== FOREIGN KEYS =====")
for fk in db.execute("PRAGMA foreign_key_list(cotacao_itens)").fetchall():
    print(fk)