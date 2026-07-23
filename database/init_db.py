from database.connection import get_db


def carregar_indicadores(cnpj):

    db = get_db()

    # =========================
    # TOTAL DE COTAÇÕES
    # =========================

    total_cotacoes = db.execute(
        """
        SELECT COUNT(*)
        FROM cotacoes
        WHERE cnpj_usuario=?
        """,
        (cnpj,)
    ).fetchone()[0]

    # =========================
    # TOTAL DE PRODUTOS
    # =========================

    total_produtos = db.execute(
        """
        SELECT COUNT(*)
        FROM cotacao_itens ci
        JOIN cotacoes c
            ON c.id = ci.cotacao_id
        WHERE c.cnpj_usuario=?
        """,
        (cnpj,)
    ).fetchone()[0]

    # =========================
    # DISTRIBUIDORAS
    # =========================

    total_distribuidoras = db.execute(
        """
        SELECT COUNT(DISTINCT distribuidora)
        FROM respostas_cotacao rc
        JOIN cotacoes c
            ON c.id = rc.cotacao_id
        WHERE c.cnpj_usuario=?
        """,
        (cnpj,)
    ).fetchone()[0]

    # =========================
    # ECONOMIA
    # =========================

    economia = db.execute(
        """
        SELECT
            SUM(maior - menor)
        FROM (

            SELECT

                medicamento,

                MAX(
                    CASE
                        WHEN preco_oferta IS NOT NULL
                        THEN preco_oferta
                        ELSE preco
                    END
                ) AS maior,

                MIN(
                    CASE
                        WHEN preco_oferta IS NOT NULL
                        THEN preco_oferta
                        ELSE preco
                    END
                ) AS menor

            FROM respostas_cotacao rc

            JOIN cotacoes c
                ON c.id = rc.cotacao_id

            WHERE c.cnpj_usuario=?

            GROUP BY medicamento

        )
        """,
        (cnpj,)
    ).fetchone()[0]

    if economia is None:
        economia = 0

    return {

        "cotacoes": total_cotacoes,

        "economia": f"R$ {economia:,.2f}".replace(",", "X").replace(".", ",").replace("X","."),

        "produtos": total_produtos,

        "distribuidoras": total_distribuidoras

    }