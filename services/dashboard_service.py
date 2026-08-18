from database.connection import get_db
from datetime import datetime


def carregar_indicadores(cnpj):

    db = get_db()

    # ==========================================
    # MÊS ATUAL
    # ==========================================

    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    mes_atual = meses[datetime.now().month - 1]

    # ==========================================
    # TOTAL DE COTAÇÕES
    # ==========================================

    total_cotacoes = db.execute(
        """
        SELECT COUNT(*)
        FROM cotacoes
        WHERE cnpj_usuario=?
        """,
        (cnpj,)
    ).fetchone()[0]

    # ==========================================
    # TOTAL DE PRODUTOS
    # ==========================================

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

    # ==========================================
    # TOTAL DE DISTRIBUIDORAS
    # ==========================================

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

    # ==========================================
    # ECONOMIA TOTAL
    # ==========================================

    economia_total = db.execute(
        """
        SELECT
            COALESCE(SUM(maior - menor), 0)
        FROM (
            SELECT
                rc.cotacao_id,
                rc.medicamento,
                MAX(
                    COALESCE(
                        rc.preco_oferta,
                        rc.preco
                    )
                ) AS maior,
                MIN(
                    COALESCE(
                        rc.preco_oferta,
                        rc.preco
                    )
                ) AS menor
            FROM respostas_cotacao rc
            JOIN cotacoes c
                ON c.id = rc.cotacao_id
            WHERE c.cnpj_usuario=?
            GROUP BY
                rc.cotacao_id,
                rc.medicamento
        )
        """,
        (cnpj,)
    ).fetchone()[0]

    # ==========================================
    # ECONOMIA DO MÊS ATUAL
    # ==========================================

    economia_mes = db.execute(
        """
        SELECT
            COALESCE(SUM(maior - menor), 0)
        FROM (
            SELECT
                rc.cotacao_id,
                rc.medicamento,
                MAX(
                    COALESCE(
                        rc.preco_oferta,
                        rc.preco
                    )
                ) AS maior,
                MIN(
                    COALESCE(
                        rc.preco_oferta,
                        rc.preco
                    )
                ) AS menor
            FROM respostas_cotacao rc
            JOIN cotacoes c
                ON c.id = rc.cotacao_id
            WHERE c.cnpj_usuario=?
              AND strftime(
                    '%Y-%m',
                    c.data_criacao
                  ) = strftime(
                    '%Y-%m',
                    'now',
                    'localtime'
                  )
            GROUP BY
                rc.cotacao_id,
                rc.medicamento
        )
        """,
        (cnpj,)
    ).fetchone()[0]

    # ==========================================
    # GARANTE ZERO
    # ==========================================

    if economia_total is None:
        economia_total = 0

    if economia_mes is None:
        economia_mes = 0

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    economia_mes_formatada = (
        f"R$ {economia_mes:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    economia_total_formatada = (
        f"R$ {economia_total:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    # ==========================================
    # RETORNO
    # ==========================================

    return {
        "cotacoes": total_cotacoes,
        "economia_mes": economia_mes_formatada,
        "economia_total": economia_total_formatada,
        "produtos": total_produtos,
        "distribuidoras": total_distribuidoras,
        "mes_atual": mes_atual
    }


def carregar_ultimas_cotacoes(cnpj):

    db = get_db()

    dados = db.execute(
        """
        SELECT
            id,
            cnpj_usuario,
            nome,
            status,
            data_criacao
        FROM cotacoes
        WHERE cnpj_usuario = ?
        ORDER BY id DESC
        LIMIT 5
        """,
        (cnpj,)
    ).fetchall()

    return dados