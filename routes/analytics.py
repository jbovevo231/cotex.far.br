print(">>> ROUTE ANALYTICS CARREGADA <<<")


from flask import (
    Blueprint,
    render_template,
    session,
    jsonify
)


from database.connection import get_db


from models.analytics import (
    buscar_cotacoes_realizadas,
    buscar_economia_gerada,
    buscar_taxa_resposta
)


analytics_bp = Blueprint(
    "analytics",
    __name__
)


# =========================================================
# PÁGINA ANALYTICS
# =========================================================

@analytics_bp.route("/analytics")
def analytics():

    if "usuario_id" not in session:

        return render_template(
            "login.html"
        )

    return render_template(
        "analytics.html"
    )


# =========================================================
# COTAÇÕES REALIZADAS
# =========================================================

@analytics_bp.route(
    "/analytics/cotacoes-realizadas"
)
def analytics_cotacoes_realizadas():

    if "usuario_id" not in session:

        return jsonify([])

    return jsonify(
        buscar_cotacoes_realizadas()
    )


# =========================================================
# ECONOMIA GERADA
# =========================================================

@analytics_bp.route(
    "/analytics/economia-gerada"
)
def analytics_economia_gerada():

    if "usuario_id" not in session:

        return jsonify([])

    return jsonify(
        buscar_economia_gerada()
    )


# =========================================================
# TAXA DE RESPOSTA
# =========================================================

@analytics_bp.route(
    "/analytics/taxa-resposta"
)
def analytics_taxa_resposta():

    if "usuario_id" not in session:

        return jsonify([])

    return jsonify(
        buscar_taxa_resposta()
    )


# =========================================================
# MEDICAMENTOS MAIS COTADOS
# =========================================================

@analytics_bp.route(
    "/analytics/medicamentos-mais-cotados"
)
def analytics_medicamentos_mais_cotados():

    if "usuario_id" not in session:

        return jsonify([])


    cnpj = session.get(
        "usuario_cnpj"
    )


    print("\n======================================")
    print(
        "ANALYTICS - MEDICAMENTOS MAIS COTADOS"
    )
    print(
        "USUARIO ID:",
        session.get("usuario_id")
    )
    print(
        "CNPJ:",
        cnpj
    )
    print("======================================")


    if not cnpj:

        print(
            "ERRO: CNPJ não encontrado na sessão"
        )

        return jsonify([])


    conn = None


    try:

        conn = get_db()

        cursor = conn.cursor()


        # =====================================================
        # BUSCA OS 10 MEDICAMENTOS MAIS COTADOS
        # EM TODAS AS COTAÇÕES DA FARMÁCIA
        # =====================================================

        cursor.execute("""
            SELECT
                ci.medicamento,
                COUNT(*) AS quantidade

            FROM cotacao_itens ci

            INNER JOIN cotacoes c
                ON c.id = ci.cotacao_id

            WHERE c.cnpj_usuario = ?

            GROUP BY ci.medicamento

            ORDER BY quantidade DESC

            LIMIT 10
        """, (cnpj,))


        dados = cursor.fetchall()


        print(
            "\n--- TOP 10 MEDICAMENTOS ---"
        )

        print(
            "TOTAL ENCONTRADO:",
            len(dados)
        )


        resultado = []


        for item in dados:

            try:

                medicamento = item[
                    "medicamento"
                ]

                quantidade = item[
                    "quantidade"
                ]


            except (
                TypeError,
                IndexError
            ):

                medicamento = item[0]

                quantidade = item[1]


            resultado.append({

                "medicamento":
                    medicamento,

                "quantidade":
                    quantidade

            })


        print(
            "\nRESULTADO FINAL:"
        )

        print(
            resultado
        )

        print(
            "======================================\n"
        )


        return jsonify(
            resultado
        )


    except Exception as e:

        import traceback

        traceback.print_exc()


        return jsonify({

            "erro": str(e)

        }), 500


    finally:

        if conn:

            conn.close()


print(
    ">>> FIM DO ARQUIVO ANALYTICS <<<"
)