from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from database.connection import get_db

from models.cotacao import (
    salvar_cotacao,
    listar_cotacoes,
    buscar_itens,
    gerar_link_cotacao
)

cotacao_bp = Blueprint("cotacao", __name__)


@cotacao_bp.route("/cotacoes")
def cotacoes():

    cnpj = session.get("usuario_cnpj")

    cotacoes = listar_cotacoes(cnpj)

    return render_template(
        "cotacoes.html",
        cotacoes=cotacoes
    )


@cotacao_bp.route("/responder/<token>")
def responder_cotacao(token):

    conn = get_db()
    cursor = conn.cursor()

    # Procura o link da cotação
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

    # Busca o nome da cotação
    cursor.execute("""
        SELECT nome
        FROM cotacoes
        WHERE id = ?
    """, (cotacao_id,))

    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return "Cotação não encontrada.", 404

    nome_cotacao = resultado[0]

    # Busca os medicamentos
    cursor.execute("""
        SELECT medicamento,
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

@cotacao_bp.route("/cotacoes/<int:id>")
def visualizar_cotacao(id):

    itens = buscar_itens(id)

    return render_template(
        "visualizar_cotacao.html",
        itens=itens,
        id=id
    )

@cotacao_bp.route("/cotacoes/<int:id>/itens")
def itens_cotacao(id):

    itens = buscar_itens(id)

    lista = []

    for item in itens:

        lista.append({
            "medicamento": item[0],
            "laboratorio": item[1],
            "quantidade": item[2]
        })

    return jsonify(lista)

@cotacao_bp.route("/cotacoes/<int:id>/gerar-link", methods=["POST"])
def gerar_link(id):

    token = gerar_link_cotacao(id)

    return jsonify({
        "sucesso": True,
        "token": token
    })

@cotacao_bp.route("/cotacoes/criar", methods=["POST"])
def criar_cotacao():

    cnpj = session.get("usuario_cnpj")

    nome = request.form.get("nome_cotacao")

    medicamentos = request.form.getlist("medicamento[]")
    laboratorios = request.form.getlist("laboratorio[]")
    quantidades = request.form.getlist("quantidade[]")

    salvar_cotacao(
        cnpj,
        nome,
        medicamentos,
        laboratorios,
        quantidades
    )

    return redirect(url_for("dashboard.dashboard"))