from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

from database.connection import get_db

from models.cotacao import (
    salvar_cotacao,
    listar_cotacoes,
    buscar_itens,
    gerar_link_cotacao,
    salvar_resposta_cotacao,
    encerrar_cotacao,
    excluir_cotacao
)


cotacao_bp = Blueprint(
    "cotacao",
    __name__
)


# =========================================================
# LISTAR COTAÇÕES
# =========================================================

@cotacao_bp.route("/cotacoes")
def cotacoes():

    cnpj = session.get("usuario_cnpj")

    cotacoes = listar_cotacoes(cnpj)

    return render_template(
        "cotacoes.html",
        cotacoes=cotacoes
    )


# =========================================================
# RESPONDER COTAÇÃO
# =========================================================

@cotacao_bp.route(
    "/responder/<token>",
    methods=["GET", "POST"]
)
def responder_cotacao(token):

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        conn = get_db()
        cursor = conn.cursor()


        # -------------------------------------------------
        # LOCALIZA A COTAÇÃO PELO TOKEN
        # -------------------------------------------------

        cursor.execute("""
            SELECT cotacao_id
            FROM links_cotacao
            WHERE token = ?
        """, (token,))


        link = cursor.fetchone()


        if not link:

            conn.close()

            return "Link inválido.", 404


        cotacao_id = link[0]

        conn.close()


        # =================================================
        # MEDICAMENTOS
        # =================================================

        medicamentos = request.form.getlist(
            "medicamento[]"
        )


        # =================================================
        # LISTAS
        # =================================================

        status = []

        precos = []

        precos_oferta = []

        quantidades_oferta = []


        # =================================================
        # LÊ CADA MEDICAMENTO INDIVIDUALMENTE
        # =================================================

        for i in range(len(medicamentos)):

            numero = i + 1


            # ---------------------------------------------
            # STATUS
            # ---------------------------------------------

            status_item = request.form.get(
                f"status{numero}",
                ""
            ).strip()


            # ---------------------------------------------
            # PREÇO NORMAL
            # ---------------------------------------------

            preco_item = request.form.get(
                f"preco{numero}",
                ""
            ).strip()


            # ---------------------------------------------
            # PREÇO OFERTA
            # ---------------------------------------------

            preco_oferta_item = request.form.get(
                f"preco_oferta{numero}",
                ""
            ).strip()


            # ---------------------------------------------
            # QUANTIDADE OFERTA
            # ---------------------------------------------

            quantidade_oferta_item = request.form.get(
                f"quantidade_oferta{numero}",
                ""
            ).strip()


            # ---------------------------------------------
            # ADICIONA ÀS LISTAS
            # ---------------------------------------------

            status.append(
                status_item
            )

            precos.append(
                preco_item
            )

            precos_oferta.append(
                preco_oferta_item
            )

            quantidades_oferta.append(
                quantidade_oferta_item
            )


        # =================================================
        # DEBUG
        # =================================================

        print("======================================")
        print("RESPOSTA DA COTAÇÃO")
        print("COTAÇÃO:", cotacao_id)
        print("======================================")


        for i in range(len(medicamentos)):

            print(
                f"MEDICAMENTO {i + 1}:",
                medicamentos[i],
                "| STATUS:",
                status[i],
                "| PREÇO:",
                precos[i],
                "| OFERTA:",
                precos_oferta[i],
                "| QTD OFERTA:",
                quantidades_oferta[i]
            )


        print("======================================")
        print("FORM COMPLETO:")
        print(request.form)
        print("======================================")


        # =================================================
        # SALVA RESPOSTA
        # =================================================

        salvar_resposta_cotacao(

            cotacao_id=cotacao_id,

            representante=request.form.get(
                "representante"
            ),

            distribuidora=request.form.get(
                "distribuidora"
            ),

            whatsapp=request.form.get(
                "whatsapp"
            ),

            medicamentos=medicamentos,

            status=status,

            precos=precos,

            precos_oferta=precos_oferta,

            quantidades_oferta=quantidades_oferta
        )


        return render_template(
            "cotacao_enviada.html",
            encerrada=False
        )


    # =====================================================
    # GET
    # =====================================================

    conn = get_db()

    cursor = conn.cursor()


    # -----------------------------------------------------
    # LOCALIZA A COTAÇÃO PELO TOKEN
    # -----------------------------------------------------

    cursor.execute("""
        SELECT cotacao_id
        FROM links_cotacao
        WHERE token = ?
    """, (token,))


    link = cursor.fetchone()


    if not link:

        conn.close()

        return "Link inválido.", 404


    cotacao_id = link[0]


    # -----------------------------------------------------
    # BUSCA NOME E STATUS
    # -----------------------------------------------------

    cursor.execute("""
        SELECT nome, status
        FROM cotacoes
        WHERE id = ?
    """, (cotacao_id,))


    resultado = cursor.fetchone()


    if not resultado:

        conn.close()

        return "Cotação não encontrada.", 404


    nome_cotacao = resultado[0]

    status_cotacao = resultado[1]


    # -----------------------------------------------------
    # COTAÇÃO ENCERRADA
    # -----------------------------------------------------

    if status_cotacao == "ENCERRADA":

        conn.close()

        return render_template(
            "cotacao_enviada.html",
            encerrada=True
        ), 403


    # -----------------------------------------------------
    # BUSCA MEDICAMENTOS
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            medicamento,
            laboratorio,
            quantidade
        FROM cotacao_itens
        WHERE cotacao_id = ?
    """, (cotacao_id,))


    itens = cursor.fetchall()


    conn.close()


    return render_template(
        "responder_cotacao.html",
        nome_cotacao=nome_cotacao,
        token=token,
        itens=itens
    )


# =========================================================
# ITENS DA COTAÇÃO
# =========================================================

@cotacao_bp.route(
    "/cotacoes/<int:id>/itens"
)
def itens_cotacao(id):

    itens = buscar_itens(id)

    lista = []


    for item in itens:

        lista.append({
            "medicamento": item[0],
            "quantidade": item[1]
        })


    return jsonify(lista)


# =========================================================
# GERAR LINK
# =========================================================

@cotacao_bp.route(
    "/cotacoes/<int:id>/gerar-link",
    methods=["POST"]
)
def gerar_link(id):

    token = gerar_link_cotacao(id)

    return jsonify({
        "sucesso": True,
        "token": token
    })


# =========================================================
# ENCERRAR COTAÇÃO
# =========================================================

@cotacao_bp.route(
    "/cotacoes/<int:id>/encerrar",
    methods=["POST"]
)
def encerrar(id):

    encerrar_cotacao(id)

    return jsonify({
        "sucesso": True
    })


# =========================================================
# EXCLUIR COTAÇÃO
# =========================================================

@cotacao_bp.route(
    "/cotacoes/<int:id>/excluir",
    methods=["POST"]
)
def excluir(id):

    try:

        excluir_cotacao(id)

        return jsonify({
            "sucesso": True
        })


    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 500


# =========================================================
# CRIAR COTAÇÃO
# =========================================================

@cotacao_bp.route(
    "/cotacoes/criar",
    methods=["POST"]
)
def criar_cotacao():

    cnpj = session.get(
        "usuario_cnpj"
    )


    nome = request.form.get(
        "nome_cotacao"
    )


    medicamentos = request.form.getlist(
        "medicamento[]"
    )


    quantidades = request.form.getlist(
        "quantidade[]"
    )


    salvar_cotacao(
        cnpj,
        nome,
        medicamentos,
        quantidades
    )


    return redirect(
        url_for("dashboard.dashboard")
    )


# =========================================================
# ENVIAR MEDICAMENTO PARA A PRÓXIMA COTAÇÃO
# =========================================================

@cotacao_bp.route(
    "/cotacoes/<int:id>/enviar-proxima-cotacao",
    methods=["POST"]
)
def enviar_proxima_cotacao(id):

    try:

        medicamento = request.form.get(
            "medicamento"
        )


        if not medicamento:

            return jsonify({
                "sucesso": False,
                "erro": "Medicamento não informado."
            }), 400


        db = get_db()


        # =================================================
        # BUSCA O MEDICAMENTO NA COTAÇÃO ATUAL
        # =================================================

        item = db.execute(
            """
            SELECT
                medicamento,
                laboratorio,
                quantidade
            FROM cotacao_itens
            WHERE cotacao_id = ?
            AND medicamento = ?
            """,
            (
                id,
                medicamento
            )
        ).fetchone()


        if not item:

            return jsonify({
                "sucesso": False,
                "erro":
                    "Medicamento não encontrado na cotação."
            }), 404


        # =================================================
        # COLOCA EM RECUPERAR PENDÊNCIA
        # =================================================

        db.execute(
            """
            INSERT INTO itens_pendentes
            (
                medicamento,
                laboratorio,
                quantidade,
                cotacao_origem
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                item[0],
                item[1],
                item[2],
                id
            )
        )


        # =================================================
        # REMOVE DA COTAÇÃO ATUAL
        # =================================================

        db.execute(
            """
            DELETE FROM cotacao_itens
            WHERE cotacao_id = ?
            AND medicamento = ?
            """,
            (
                id,
                medicamento
            )
        )


        db.commit()


        return jsonify({
            "sucesso": True,
            "mensagem":
                "Medicamento enviado para a próxima cotação."
        })


    except Exception as e:

        import traceback

        traceback.print_exc()


        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 500