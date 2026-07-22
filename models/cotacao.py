from database.connection import get_db
import uuid


def salvar_cotacao(cnpj, nome, medicamentos, laboratorios, quantidades):
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO cotacoes (
            cnpj_usuario,
            nome,
            status
        )
        VALUES (?, ?, 'RASCUNHO')
        """,
        (cnpj, nome)
    )

    cotacao_id = cursor.lastrowid

    for medicamento, laboratorio, quantidade in zip(
        medicamentos,
        laboratorios,
        quantidades
    ):

        db.execute(
            """
            INSERT INTO cotacao_itens (
                cotacao_id,
                medicamento,
                laboratorio,
                quantidade
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                cotacao_id,
                medicamento,
                laboratorio,
                quantidade
            )
        )

    db.commit()

    return cotacao_id


def listar_cotacoes(cnpj):
    db = get_db()

    return db.execute(
        """
        SELECT
            id,
            nome,
            status,
            data_criacao
        FROM cotacoes
        WHERE cnpj_usuario = ?
        ORDER BY id DESC
        """,
        (cnpj,)
    ).fetchall()

    
def buscar_itens(cotacao_id):
    db = get_db()

    return db.execute(
        """
        SELECT
            medicamento,
            laboratorio,
            quantidade
        FROM cotacao_itens
        WHERE cotacao_id = ?
        ORDER BY id
        """,
        (cotacao_id,)
    ).fetchall()


def gerar_link_cotacao(cotacao_id):

    db = get_db()

    # Verifica se a cotação já possui um link
    link = db.execute(
        """
        SELECT token
        FROM links_cotacao
        WHERE cotacao_id = ?
        LIMIT 1
        """,
        (cotacao_id,)
    ).fetchone()

    if link:
        return link[0]

    # Gera um token único
    token = uuid.uuid4().hex

    db.execute(
        """
        INSERT INTO links_cotacao (
            cotacao_id,
            token
        )
        VALUES (?, ?)
        """,
        (
            cotacao_id,
            token
        )
    )

    db.commit()

    return token

def salvar_resposta_cotacao(
    cotacao_id,
    representante,
    distribuidora,
    whatsapp,
    medicamentos,
    status,
    precos,
    precos_oferta,
    quantidades_oferta
):

    db = get_db()

    for i in range(len(medicamentos)):

        preco = None
        preco_oferta = None
        quantidade_oferta = None

        if i < len(precos) and precos[i]:
            preco = precos[i].replace(",", ".")

        if i < len(precos_oferta) and precos_oferta[i]:
            preco_oferta = precos_oferta[i].replace(",", ".")

        if i < len(quantidades_oferta) and quantidades_oferta[i]:
            quantidade_oferta = quantidades_oferta[i]

        db.execute(
            """
            INSERT INTO respostas_cotacao (
                cotacao_id,
                medicamento,
                representante,
                distribuidora,
                whatsapp,
                status,
                preco,
                preco_oferta,
                quantidade_oferta
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cotacao_id,
                medicamentos[i],
                representante,
                distribuidora,
                whatsapp,
                status[i] if i < len(status) else "",
                preco,
                preco_oferta,
                quantidade_oferta
            )
        )

    db.commit()
    db.close()