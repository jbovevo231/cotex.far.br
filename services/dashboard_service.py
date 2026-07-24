from database.connection import get_db


def carregar_indicadores(cnpj):

    db = get_db()

    # Total de cotações
    total_cotacoes = db.execute(
        """
        SELECT COUNT(*)
        FROM cotacoes
        WHERE cnpj_usuario=?
        """,
        (cnpj,)
    ).fetchone()[0]

    # Total de produtos
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

    # Total de distribuidoras
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

    # Economia Total
    economia_total = db.execute(
        """
        SELECT
            COALESCE(SUM(maior - menor),0)
        FROM (
            SELECT
                rc.cotacao_id,
                rc.medicamento,
                MAX(COALESCE(rc.preco_oferta, rc.preco)) AS maior,
                MIN(COALESCE(rc.preco_oferta, rc.preco)) AS menor
            FROM respostas_cotacao rc
            JOIN cotacoes c
                ON c.id = rc.cotacao_id
            WHERE c.cnpj_usuario=?
            GROUP BY rc.cotacao_id, rc.medicamento
        )
        """,
        (cnpj,)
    ).fetchone()[0]

    # Economia do Mês
    economia_mes = db.execute(
        """
        SELECT
            COALESCE(SUM(maior - menor),0)
        FROM (
            SELECT
                rc.cotacao_id,
                rc.medicamento,
                MAX(COALESCE(rc.preco_oferta, rc.preco)) AS maior,
                MIN(COALESCE(rc.preco_oferta, rc.preco)) AS menor
            FROM respostas_cotacao rc
            JOIN cotacoes c
                ON c.id = rc.cotacao_id
            WHERE c.cnpj_usuario=?
              AND strftime('%Y-%m', c.data_criacao) = strftime('%Y-%m', 'now', 'localtime')
            GROUP BY rc.cotacao_id, rc.medicamento
        )
        """,
        (cnpj,)
    ).fetchone()[0]

    if economia_total is None:
        economia_total = 0

    if economia_mes is None:
        economia_mes = 0

    return {
        "cotacoes": total_cotacoes,
        "economia_mes": f"R$ {economia_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "economia_total": f"R$ {economia_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "produtos": total_produtos,
        "distribuidoras": total_distribuidoras
    }


def carregar_ultimas_cotacoes(cnpj):

    db = get_db()

    dados = db.execute(
        """
        SELECT *
        FROM cotacoes
        WHERE cnpj_usuario=?
        ORDER BY id DESC
        LIMIT 5
        """,
        (cnpj,)
    ).fetchall()

    return dados