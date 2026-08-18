from flask import session
from database.connection import get_db


# =========================================================
# CNPJ DA FARMÁCIA LOGADA
# =========================================================

def obter_cnpj_usuario():

    cnpj = session.get("usuario_cnpj")

    if not cnpj:
        return None

    return cnpj


# =========================================================
# COTAÇÕES REALIZADAS
# =========================================================

def buscar_cotacoes_realizadas(data_inicio=None, data_fim=None):

    cnpj = obter_cnpj_usuario()

    if not cnpj:
        return []

    db = get_db()

    try:

        sql = """
            SELECT
                DATE(data_criacao) AS dia,
                COUNT(*) AS total

            FROM cotacoes

            WHERE cnpj_usuario = ?
        """

        parametros = [cnpj]

        # -----------------------------------------
        # DATA INICIAL
        # -----------------------------------------

        if data_inicio:

            sql += """
                AND DATE(data_criacao) >= DATE(?)
            """

            parametros.append(data_inicio)

        # -----------------------------------------
        # DATA FINAL
        # -----------------------------------------

        if data_fim:

            sql += """
                AND DATE(data_criacao) <= DATE(?)
            """

            parametros.append(data_fim)

        sql += """
            GROUP BY DATE(data_criacao)

            ORDER BY DATE(data_criacao)
        """

        cursor = db.execute(
            sql,
            parametros
        )

        dados = cursor.fetchall()

        resultado = []

        for item in dados:

            resultado.append({
                "dia": item[0],
                "total": int(item[1] or 0)
            })

        return resultado

    finally:

        db.close()


# =========================================================
# ECONOMIA GERADA
# =========================================================

def buscar_economia_gerada(data_inicio=None, data_fim=None):

    cnpj = obter_cnpj_usuario()

    if not cnpj:
        return []

    db = get_db()

    try:

        sql = """
            SELECT

                DATE(c.data_criacao) AS dia,

                SUM(
                    maior - menor
                ) AS total

            FROM (

                SELECT

                    rc.cotacao_id,

                    rc.medicamento,

                    MAX(
                        CASE
                            WHEN rc.preco_oferta IS NOT NULL
                            THEN rc.preco_oferta
                            ELSE rc.preco
                        END
                    ) AS maior,

                    MIN(
                        CASE
                            WHEN rc.preco_oferta IS NOT NULL
                            THEN rc.preco_oferta
                            ELSE rc.preco
                        END
                    ) AS menor

                FROM respostas_cotacao rc

                JOIN cotacoes c

                    ON c.id = rc.cotacao_id

                WHERE c.cnpj_usuario = ?

                GROUP BY

                    rc.cotacao_id,
                    rc.medicamento

            ) x

            JOIN cotacoes c

                ON c.id = x.cotacao_id

            WHERE 1=1
        """

        parametros = [cnpj]

        # -----------------------------------------
        # DATA INICIAL
        # -----------------------------------------

        if data_inicio:

            sql += """
                AND DATE(c.data_criacao) >= DATE(?)
            """

            parametros.append(data_inicio)

        # -----------------------------------------
        # DATA FINAL
        # -----------------------------------------

        if data_fim:

            sql += """
                AND DATE(c.data_criacao) <= DATE(?)
            """

            parametros.append(data_fim)

        sql += """
            GROUP BY DATE(c.data_criacao)

            ORDER BY DATE(c.data_criacao)
        """

        cursor = db.execute(
            sql,
            parametros
        )

        dados = cursor.fetchall()

        resultado = []

        for item in dados:

            resultado.append({
                "dia": item[0],
                "total": float(item[1] or 0)
            })

        return resultado

    finally:

        db.close()


# =========================================================
# TAXA DE RESPOSTA
# =========================================================

def buscar_taxa_resposta(data_inicio=None, data_fim=None):

    cnpj = obter_cnpj_usuario()

    if not cnpj:
        return []

    db = get_db()

    try:

        sql = """
            SELECT

                DATE(c.data_criacao) AS dia,

                ROUND(

                    (
                        COUNT(DISTINCT rc.representante)
                        * 100.0
                    )

                    /

                    NULLIF(
                        COUNT(DISTINCT cr.representante_id),
                        0
                    ),

                    2

                ) AS total

            FROM cotacoes c

            LEFT JOIN cotacao_representante cr

                ON cr.cotacao_id = c.id

            LEFT JOIN respostas_cotacao rc

                ON rc.cotacao_id = c.id

            WHERE c.cnpj_usuario = ?
        """

        parametros = [cnpj]

        # -----------------------------------------
        # DATA INICIAL
        # -----------------------------------------

        if data_inicio:

            sql += """
                AND DATE(c.data_criacao) >= DATE(?)
            """

            parametros.append(data_inicio)

        # -----------------------------------------
        # DATA FINAL
        # -----------------------------------------

        if data_fim:

            sql += """
                AND DATE(c.data_criacao) <= DATE(?)
            """

            parametros.append(data_fim)

        sql += """
            GROUP BY DATE(c.data_criacao)

            ORDER BY DATE(c.data_criacao)
        """

        cursor = db.execute(
            sql,
            parametros
        )

        dados = cursor.fetchall()

        resultado = []

        for item in dados:

            resultado.append({
                "dia": item[0],
                "total": float(item[1] or 0)
            })

        return resultado

    finally:

        db.close()