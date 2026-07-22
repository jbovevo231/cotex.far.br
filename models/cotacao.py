from database.connection import get_db


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