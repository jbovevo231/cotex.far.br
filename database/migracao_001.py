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

# ==========================================
# CONECTA - POSTS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS conecta_posts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cnpj TEXT NOT NULL,

    usuario TEXT NOT NULL,

    texto TEXT,

    imagem TEXT,

    data_postagem TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# ==========================================
# HISTÓRICO DE MEDICAMENTOS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS historico_medicamentos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cnpj_usuario TEXT NOT NULL,

    medicamento TEXT NOT NULL,

    laboratorio TEXT,

    vezes INTEGER DEFAULT 1,

    ultima_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# ==========================================
# STATUS DAS CONTAS DE USUÁRIOS
# ==========================================

try:

    colunas = cursor.execute(
        "PRAGMA table_info(usuarios)"
    ).fetchall()

    nomes_colunas = [coluna[1] for coluna in colunas]

    if "status" not in nomes_colunas:

        cursor.execute("""
            ALTER TABLE usuarios
            ADD COLUMN status TEXT DEFAULT 'ativo'
        """)

        print("✅ Coluna status adicionada à tabela usuarios.")

    else:

        print("ℹ️ Coluna status já existe.")

except Exception as e:

    print("❌ Erro ao verificar/adicionar status:")
    print(e)


# ==========================================
# SALVAR ALTERAÇÕES
# ==========================================

try:

    conn.commit()

    print("✅ Tabelas criadas/atualizadas com sucesso!")

except Exception as e:

    print("❌ ERRO NO COMMIT:")
    print(e)


conn.close()

# ==========================================
# STATUS DAS CONTAS DE USUÁRIOS
# ==========================================

try:

    cursor.execute("""
        ALTER TABLE usuarios
        ADD COLUMN status TEXT DEFAULT 'ativo'
    """)

    print("✅ Coluna status adicionada à tabela usuarios.")

except Exception as e:

    if "duplicate column name" in str(e).lower():
        print("ℹ️ Coluna status já existe.")

    else:
        print("❌ Erro ao adicionar coluna status:")
        print(e)