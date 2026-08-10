from flask import Blueprint, jsonify, request
import sqlite3

from database.connection import get_db
from models.comparativo import buscar_comparativo, buscar_resultado


print(">>> ROUTE COMPARATIVO CARREGADA <<<")

comparativo_bp = Blueprint("comparativo", __name__)

@comparativo_bp.route("/comparativo/<int:cotacao_id>")
def comparativo(cotacao_id):

    dados = buscar_comparativo(cotacao_id)

    return jsonify(dados)

@comparativo_bp.route("/resultado/<int:cotacao_id>")
def resultado(cotacao_id):

    dados = buscar_resultado(cotacao_id)

    return jsonify(dados)

# =====================================================
# PRÓXIMO MELHOR PREÇO
# =====================================================

@comparativo_bp.route(
    "/cotacoes/<int:cotacao_id>/proximo-melhor-preco",
    methods=["POST"]
)
def proximo_melhor_preco(cotacao_id):

    medicamento = request.form.get(
        "medicamento",
        ""
    ).strip()

    representante_atual = request.form.get(
        "representante_atual"
    )

    if not medicamento:
        return jsonify({
            "sucesso": False,
            "erro": "Medicamento não informado."
        }), 400

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:

        # =================================================
        # BUSCA TODOS OS PREÇOS DO MEDICAMENTO
        # =================================================

        cursor.execute("""
            SELECT
                r.representante_id,
                r.medicamento,
                r.preco,
                r.oferta,
                r.quantidade_oferta,
                rep.nome AS representante,
                rep.distribuidora

            FROM respostas r

            INNER JOIN representantes rep
                ON rep.id = r.representante_id

            WHERE r.cotacao_id = ?
              AND LOWER(TRIM(r.medicamento))
                  = LOWER(TRIM(?))
              AND r.preco > 0

            ORDER BY r.preco ASC
        """, (
            cotacao_id,
            medicamento
        ))

        respostas = cursor.fetchall()

        if not respostas:

            return jsonify({
                "sucesso": False,
                "erro":
                    "Nenhum representante respondeu este medicamento."
            })

        # =================================================
        # ENCONTRA O PRÓXIMO PREÇO
        # =================================================

        proximo = None

        for resposta in respostas:

            if (
                representante_atual
                and str(resposta["representante_id"])
                    == str(representante_atual)
            ):
                continue

            proximo = resposta
            break

        if not proximo:

            return jsonify({
                "sucesso": False,
                "erro":
                    "Não existe outro preço disponível."
            })

        # =================================================
        # BUSCA A QUANTIDADE ORIGINAL
        # =================================================

        cursor.execute("""
            SELECT quantidade
            FROM itens
            WHERE cotacao_id = ?
              AND LOWER(TRIM(medicamento))
                  = LOWER(TRIM(?))
            LIMIT 1
        """, (
            cotacao_id,
            medicamento
        ))

        item = cursor.fetchone()

        quantidade = (
            item["quantidade"]
            if item
            else 1
        )

        # =================================================
        # RETORNA O PRÓXIMO REPRESENTANTE
        # =================================================

        return jsonify({

            "sucesso": True,

            "representante_id":
                proximo["representante_id"],

            "representante":
                proximo["representante"],

            "distribuidora":
                proximo["distribuidora"],

            "medicamento":
                proximo["medicamento"],

            "preco":
                float(proximo["preco"]),

            "oferta":
                bool(proximo["oferta"]),

            "preco_oferta":
                float(proximo["preco"])
                if proximo["oferta"]
                else None,

            "quantidade_oferta":
                proximo["quantidade_oferta"],

            "quantidade":
                quantidade
        })

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 500

    finally:

        conn.close()