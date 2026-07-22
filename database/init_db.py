from database.connection import get_db

conn = get_db()
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = OFF")

# ===========================
# APAGA AS TABELAS ANTIGAS
# ===========================

cursor.execute("DROP TABLE IF EXISTS respostas_cotacao")
cursor.execute("DROP TABLE IF EXISTS links_cotacao")
cursor.execute("DROP TABLE IF EXISTS cotacao_itens")
cursor.execute("DROP TABLE IF EXISTS cotacoes")

# ===========================
# TABELA DE COTAÇÕES
# ===========================

cursor.execute("""
CREATE TABLE cotacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnpj_usuario TEXT NOT NULL,
    nome TEXT,
    status TEXT DEFAULT 'RASCUNHO',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ===========================
# LINKS DA COTAÇÃO
# ===========================

cursor.execute("""
CREATE TABLE links_cotacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cotacao_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cotacao_id) REFERENCES cotacoes(id)
)
""")

# ===========================
# ITENS DA COTAÇÃO
# ===========================

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

# ===========================
# RESPOSTAS DOS REPRESENTANTES
# ===========================

cursor.execute("""
CREATE TABLE respostas_cotacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cotacao_id INTEGER NOT NULL,

    medicamento TEXT NOT NULL,

    representante TEXT NOT NULL,

    distribuidora TEXT,

    whatsapp TEXT,

    status TEXT,

    preco REAL,

    preco_oferta REAL,

    quantidade_oferta INTEGER,

    data_resposta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (cotacao_id) REFERENCES cotacoes(id)
)
""")

# ===========================
# SALVA AS ALTERAÇÕES
# ===========================

cursor.execute("PRAGMA foreign_keys = ON")

conn.commit()

conn.close()

print("Tabelas recriadas com sucesso!")