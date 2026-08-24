import pandas as pd
from database.connection import get_db

print("Importando CMED para o Turso...")

df = pd.read_excel("cmed.xlsx")

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

cursor.execute("DELETE FROM tabela_cmed")
db.commit()

dados = []

for _, row in df.iterrows():

    try:
        pf = float(row.get("PF Sem Impostos"))
    except:
        pf = None

    try:
        pmc = float(row.get("PMC Sem Impostos"))
    except:
        pmc = None

    dados.append((
        str(row.get("PRINCÍPIO ATIVO", "")).strip(),
        str(row.get("APRESENTAÇÃO", "")).strip(),
        str(row.get("LABORATÓRIO", "")).strip(),
        pf,
        pmc
    ))

# envia em lotes de 500
for i in range(0, len(dados), 500):
    cursor.executemany("""
        INSERT INTO tabela_cmed (
            principio_ativo,
            apresentacao,
            laboratorio,
            pf,
            pmc
        )
        VALUES (?, ?, ?, ?, ?)
    """, dados[i:i+500])
    db.commit()

cursor.execute("SELECT COUNT(*) FROM tabela_cmed")
print("Total gravado:", cursor.fetchone()[0])

db.close()

print("Importação concluída.")