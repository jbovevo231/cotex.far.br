import pandas as pd
from database.connection import get_db

print("Importando CMED para o Turso...")

# Lê a planilha
df = pd.read_excel("cmed.xlsx")
df.columns = [str(c).strip() for c in df.columns]

print("\nColunas encontradas:")
for c in df.columns:
    print("-", c)

# Conexão Turso
db = get_db()
cursor = db.cursor()

# Cria a tabela
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

# Limpa a tabela antes da nova importação
cursor.execute("DELETE FROM tabela_cmed")
db.commit()

# Colunas da planilha
COL_SUBSTANCIA = "SUBSTÂNCIA"
COL_PRODUTO = "PRODUTO"
COL_APRESENTACAO = "APRESENTAÇÃO"
COL_LAB = "LABORATÓRIO"
COL_PF = "PF Sem Impostos"
COL_PMC = "PMC Sem Impostos"

# Converte número brasileiro
def numero_br(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip()

    if valor == "" or valor.lower() == "nan":
        return None

    valor = valor.replace(".", "").replace(",", ".")

    try:
        return float(valor)
    except:
        return None

total = len(df)

print(f"\nInserindo {total} registros...\n")

for i, row in df.iterrows():

    principio = str(row[COL_SUBSTANCIA]).strip()

    # Ignora linhas vazias
    if principio == "" or principio.lower() == "nan":
        continue

    produto = str(row[COL_PRODUTO]).strip()
    apresentacao = str(row[COL_APRESENTACAO]).strip()

    # Junta produto + apresentação
    apresentacao_final = f"{produto} • {apresentacao}"

    laboratorio = str(row[COL_LAB]).strip()

    pf = numero_br(row[COL_PF])
    pmc = numero_br(row[COL_PMC])

    cursor.execute("""
        INSERT INTO tabela_cmed (
            principio_ativo,
            apresentacao,
            laboratorio,
            pf,
            pmc
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        principio,
        apresentacao_final,
        laboratorio,
        pf,
        pmc
    ))

    if (i + 1) % 100 == 0:
        db.commit()
        print(f"{i+1}/{total}")

db.commit()

cursor.execute("SELECT COUNT(*) FROM tabela_cmed")
total_gravado = cursor.fetchone()[0]

db.close()

print(f"\nTotal gravado: {total_gravado}")
print("Importação concluída com sucesso.")