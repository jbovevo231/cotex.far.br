from flask import Blueprint, jsonify
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