from database.connection import get_db


def buscar_cotacoes_realizadas():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            DATE(data_criacao) AS dia,
            COUNT(*) AS total
        FROM cotacoes
        GROUP BY DATE(data_criacao)
        ORDER BY DATE(data_criacao)
    """)

    dados = cursor.fetchall()

    db.close()

    resultado = []

    for item in dados:
        resultado.append({
            "dia": item[0],
            "total": item[1]
        })

    return resultado


def buscar_economia_gerada():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""

        SELECT

            DATE(c.data_criacao) AS dia,

            SUM(maior - menor) AS total

        FROM (

            SELECT

                cotacao_id,

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

            FROM respostas_cotacao

            GROUP BY
                cotacao_id,
                medicamento

        ) x

        JOIN cotacoes c
            ON c.id = x.cotacao_id

        GROUP BY DATE(c.data_criacao)

        ORDER BY DATE(c.data_criacao)

    """)

    dados = cursor.fetchall()

    db.close()

    resultado = []

    for item in dados:

        resultado.append({

            "dia": item[0],

            "total": float(item[1] or 0)

        })

    return resultado


def buscar_taxa_resposta():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""

        SELECT

            DATE(c.data_criacao) AS dia,

            ROUND(

                (
                    COUNT(DISTINCT rc.representante) * 100.0
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

        GROUP BY
            DATE(c.data_criacao)

        ORDER BY
            DATE(c.data_criacao)

    """)

    dados = cursor.fetchall()

    db.close()

    resultado = []

    for item in dados:

        resultado.append({

            "dia": item[0],

            "total": float(item[1] or 0)

        })

    return resultado