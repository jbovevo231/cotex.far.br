from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

from models.cotacao import (
    salvar_cotacao,
    listar_cotacoes,
    buscar_itens
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