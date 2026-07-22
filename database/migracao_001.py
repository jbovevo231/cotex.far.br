from database.connection import get_db

conn = get_db()
cursor = conn.cursor()

# ==========================================
# LINKS DAS COTAÇÕES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS links_cotacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cotacao_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    ativo INTEGER DEFAULT 1,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (cotacao_id)
    REFERENCES cotacoes(id)
)
""")

# ==========================================
# DADOS DO REPRESENTANTE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS respostas_cotacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    link_id INTEGER NOT NULL,

    nome_representante TEXT NOT NULL,

    distribuidora TEXT NOT NULL,

    telefone TEXT NOT NULL,

    enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (link_id)
    REFERENCES links_cotacao(id)
)
""")

# ==========================================
# RESPOSTA DOS ITENS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS respostas_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resposta_id INTEGER NOT NULL,

    item_cotacao_id INTEGER NOT NULL,

    possui INTEGER NOT NULL DEFAULT 0,

    valor_unitario REAL,

    valor_oferta REAL,

    quantidade_oferta INTEGER,

    FOREIGN KEY (resposta_id)
    REFERENCES respostas_cotacao(id),

    FOREIGN KEY (item_cotacao_id)
    REFERENCES cotacao_itens(id)
)
""")

conn.commit()
conn.close()

print("✅ Migração executada com sucesso!")