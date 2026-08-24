from database.connection import get_db

db = get_db()
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tabela_cmed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    principio_ativo TEXT,
    apresentacao TEXT,
    laboratorio TEXT,
    pf REAL,
    pmc REAL
)
""")

db.commit()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
  AND name='tabela_cmed'
""")

print(cursor.fetchone())

db.close()