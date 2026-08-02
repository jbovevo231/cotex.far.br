from database.connection import get_db
import uuid


def salvar_cotacao(cnpj, nome, medicamentos, quantidades):

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO cotacoes (
            cnpj_usuario,
            nome,
            status
        )
        VALUES (?, ?, 'ABERTA')
        """,
        (cnpj, nome)
    )

    cotacao_id = cursor.lastrowid

    for medicamento, quantidade in zip(
    medicamentos,
    quantidades
):

        linhas = [
            linha.strip()
            for linha in medicamento.splitlines()
            if linha.strip()
        ]

        if not linhas:
            linhas = [medicamento]

        for med in linhas:

            db.execute(
    """
    INSERT INTO cotacao_itens (
        cotacao_id,
        medicamento,
        quantidade
    )
    VALUES (?, ?, ?)
    """,
    (
        cotacao_id,
        med,
        quantidade
    )
)

            historico = db.execute(
    """
    SELECT
        id,
        vezes
    FROM historico_medicamentos
    WHERE cnpj_usuario=?
    AND medicamento=?
    """,
    (
        cnpj,
        med
    )
).fetchone()

            if historico:

                db.execute(
                    """
                    UPDATE historico_medicamentos
                    SET
                        vezes=?,
                        ultima_data=CURRENT_TIMESTAMP
                    WHERE id=?
                    """,
                    (
                        historico[1] + 1,
                        historico[0]
                    )
                )

            else:

                db.execute(
    """
    INSERT INTO historico_medicamentos(
        cnpj_usuario,
        medicamento
    )
    VALUES (?, ?)
    """,
    (
        cnpj,
        med
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


def encerrar_cotacao(cotacao_id):

    db = get_db()

    db.execute(
        """
        UPDATE cotacoes
        SET status='ENCERRADA'
        WHERE id=?
        """,
        (cotacao_id,)
    )

    db.commit()
    db.close()


def excluir_cotacao(cotacao_id):

    db = get_db()

    # Primeiro apaga as respostas dos representantes
    db.execute(
        "DELETE FROM respostas_cotacao WHERE cotacao_id=?",
        (cotacao_id,)
    )

    # Depois apaga os itens da cotação
    db.execute(
        "DELETE FROM cotacao_itens WHERE cotacao_id=?",
        (cotacao_id,)
    )

    # Depois apaga o link
    db.execute(
        "DELETE FROM links_cotacao WHERE cotacao_id=?",
        (cotacao_id,)
    )

    # Por último apaga a cotação
    db.execute(
        "DELETE FROM cotacoes WHERE id=?",
        (cotacao_id,)
    )

    db.commit()
    db.close()


def buscar_pendencias(cnpj):

    db = get_db()

    return db.execute(
        """
        SELECT
            ci.medicamento,
            ci.laboratorio,
            ci.quantidade

        FROM cotacao_itens ci

        WHERE ci.cotacao_id = (

            SELECT id

            FROM cotacoes

            WHERE status='ENCERRADA'
            AND cnpj_usuario=?

            ORDER BY id DESC

            LIMIT 1

        )

        AND NOT EXISTS (

            SELECT 1

            FROM respostas_cotacao rc

            WHERE rc.cotacao_id = ci.cotacao_id

            AND rc.medicamento = ci.medicamento

            AND rc.preco IS NOT NULL

            AND rc.preco > 0

        )

        ORDER BY ci.medicamento
        """,
        (cnpj,)
    ).fetchall()


def buscar_historico(cnpj, termo):

    db = get_db()

    return db.execute(
        """
        SELECT
            medicamento,
            laboratorio

        FROM historico_medicamentos

        WHERE cnpj_usuario=?

        AND LOWER(medicamento) LIKE LOWER(?)

        ORDER BY
            vezes DESC,
            ultima_data DESC

        LIMIT 8
        """,
        (
            cnpj,
            termo + "%"
        )
    ).fetchall()

    