from database.connection import get_db

conn = get_db()
cursor = conn.cursor()

# Apaga as tabelas antigas
cursor.execute("DROP TABLE IF EXISTS cotacao_itens")
cursor.execute("DROP TABLE IF EXISTS cotacoes")

# Cria novamente
cursor.execute("""
CREATE TABLE cotacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnpj_usuario TEXT NOT NULL,
    nome TEXT,
    status TEXT DEFAULT 'RASCUNHO',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE cotacao_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cotacao_id INTEGER NOT NULL,
    medicamento TEXT NOT NULL,
    laboratorio TEXT,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (cotacao_id) REFERENCES cotacoes(id)
)
""")

conn.commit()

print("Tabelas recriadas com sucesso!")