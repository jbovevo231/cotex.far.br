print(">>> ROUTE ANALYTICS CARREGADA <<<")


from flask import (
    Blueprint,
    render_template,
    session,
    jsonify,
    request
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

    data_inicio = request.args.get(
        "data_inicio"
    )

    data_fim = request.args.get(
        "data_fim"
    )

    return jsonify(
        buscar_cotacoes_realizadas(
            data_inicio,
            data_fim
        )
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

    data_inicio = request.args.get(
        "data_inicio"
    )

    data_fim = request.args.get(
        "data_fim"
    )

    return jsonify(
        buscar_economia_gerada(
            data_inicio,
            data_fim
        )
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

    data_inicio = request.args.get(
        "data_inicio"
    )

    data_fim = request.args.get(
        "data_fim"
    )

    return jsonify(
        buscar_taxa_resposta(
            data_inicio,
            data_fim
        )
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


    # =====================================================
    # PERÍODO SELECIONADO NO ANALYTICS
    # =====================================================

    data_inicio = request.args.get(
        "data_inicio"
    )

    data_fim = request.args.get(
        "data_fim"
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

            AND (
                    ? IS NULL
                    OR DATE(c.data_criacao) >= DATE(?)
                )

            AND (
                    ? IS NULL
                    OR DATE(c.data_criacao) <= DATE(?)
                )

            GROUP BY ci.medicamento

            ORDER BY quantidade DESC

            LIMIT 10

        """, (
            cnpj,
            data_inicio,
            data_inicio,
            data_fim,
            data_fim
        ))


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


# =========================================================
# DISTRIBUIÇÃO DOS STATUS DAS RESPOSTAS
# =========================================================

@analytics_bp.route(
    "/analytics/status"
)
def analytics_status():

    print("\n======================================")
    print(
        "ANALYTICS - DISTRIBUIÇÃO DOS STATUS"
    )
    print("======================================")


    # -----------------------------------------------------
    # VERIFICA LOGIN
    # -----------------------------------------------------

    if "usuario_id" not in session:

        print(
            "ERRO: usuário não está logado"
        )

        return jsonify({

            "labels": [
                "Tenho",
                "Tenho oferta",
                "Não tenho"
            ],

            "valores": [
                0,
                0,
                0
            ],

            "total": 0,

            "tenho": 0,

            "oferta": 0,

            "nao_tenho": 0

        })


    # -----------------------------------------------------
    # CNPJ DA FARMÁCIA
    # -----------------------------------------------------

    cnpj = session.get(
        "usuario_cnpj"
    )


    print(
        "USUARIO ID:",
        session.get("usuario_id")
    )

    print(
        "CNPJ:",
        cnpj
    )


    if not cnpj:

        print(
            "ERRO: CNPJ não encontrado na sessão"
        )

        return jsonify({

            "labels": [
                "Tenho",
                "Tenho oferta",
                "Não tenho"
            ],

            "valores": [
                0,
                0,
                0
            ],

            "total": 0,

            "tenho": 0,

            "oferta": 0,

            "nao_tenho": 0

        })


    # -----------------------------------------------------
    # DATAS OPCIONAIS
    # -----------------------------------------------------

    data_inicio = request.args.get(
        "data_inicio"
    )

    data_fim = request.args.get(
        "data_fim"
    )


    print(
        "DATA INÍCIO:",
        data_inicio
    )

    print(
        "DATA FIM:",
        data_fim
    )


    db = None


    try:

        db = get_db()


        # -------------------------------------------------
        # CONSULTA
        # -------------------------------------------------

        sql = """

            SELECT
                rc.status,
                COUNT(*) AS quantidade

            FROM respostas_cotacao rc

            INNER JOIN cotacoes c
                ON c.id = rc.cotacao_id

            WHERE c.cnpj_usuario = ?

        """


        parametros = [
            cnpj
        ]


        # -------------------------------------------------
        # FILTRO DATA INICIAL
        # -------------------------------------------------

        if data_inicio:

            sql += """

                AND date(c.data_criacao)
                    >= date(?)

            """

            parametros.append(
                data_inicio
            )


        # -------------------------------------------------
        # FILTRO DATA FINAL
        # -------------------------------------------------

        if data_fim:

            sql += """

                AND date(c.data_criacao)
                    <= date(?)

            """

            parametros.append(
                data_fim
            )


        # -------------------------------------------------
        # AGRUPAMENTO
        # -------------------------------------------------

        sql += """

            GROUP BY rc.status

        """


        print("\nSQL STATUS:")
        print(sql)

        print(
            "PARÂMETROS:",
            parametros
        )


        registros = db.execute(
            sql,
            parametros
        ).fetchall()


        print(
            "REGISTROS ENCONTRADOS:",
            len(registros)
        )


        # -------------------------------------------------
        # CONTADORES
        # -------------------------------------------------

        tenho = 0

        oferta = 0

        nao_tenho = 0


        # -------------------------------------------------
        # PROCESSA OS STATUS
        # -------------------------------------------------

        for registro in registros:

            status = registro[0]

            quantidade = (
                registro[1] or 0
            )


            print(
                "STATUS:",
                status,
                "| QUANTIDADE:",
                quantidade
            )


            if status == "TENHO":

                tenho = quantidade


            elif status == "OFERTA":

                oferta = quantidade


            elif status == "NAO_TENHO":

                nao_tenho = quantidade


        # -------------------------------------------------
        # TOTAL
        # -------------------------------------------------

        total = (

            tenho
            + oferta
            + nao_tenho

        )


        print(
            "TENHO:",
            tenho
        )

        print(
            "OFERTA:",
            oferta
        )

        print(
            "NÃO TENHO:",
            nao_tenho
        )

        print(
            "TOTAL:",
            total
        )


        # -------------------------------------------------
        # ENVIA PARA O JAVASCRIPT
        # -------------------------------------------------

        return jsonify({

            "labels": [

                "Tenho",

                "Tenho oferta",

                "Não tenho"

            ],

            "valores": [

                tenho,

                oferta,

                nao_tenho

            ],

            "total": total,

            "tenho": tenho,

            "oferta": oferta,

            "nao_tenho": nao_tenho

        })


    except Exception as e:

        import traceback

        traceback.print_exc()


        return jsonify({

            "labels": [

                "Tenho",

                "Tenho oferta",

                "Não tenho"

            ],

            "valores": [

                0,

                0,

                0

            ],

            "total": 0,

            "tenho": 0,

            "oferta": 0,

            "nao_tenho": 0,

            "erro": str(e)

        }), 500


    finally:

        if db:

            db.close()


# =========================================================
# FIM
# =========================================================

print(
    ">>> FIM DO ARQUIVO ANALYTICS <<<"
)