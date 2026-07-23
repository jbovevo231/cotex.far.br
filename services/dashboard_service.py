from database.connection import get_db


def carregar_indicadores(cnpj):

    db = get_db()

    total_cotacoes = db.execute(
        """
        SELECT COUNT(*)
        FROM cotacoes
        WHERE cnpj_usuario=?
        """,
        (cnpj,)
    ).fetchone()[0]

    return {
        "cotacoes": total_cotacoes,
        "economia": "R$ 0,00",
        "produtos": 0,
        "distribuidoras": 0
    }


def carregar_ultimas_cotacoes(cnpj):

    db = get_db()

    print("CNPJ recebido:", cnpj)

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

    print("Últimas cotações:", dados)

    return dados