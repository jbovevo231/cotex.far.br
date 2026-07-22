from flask import Blueprint, jsonify
from models.comparativo import buscar_comparativo

print(">>> ROUTE COMPARATIVO CARREGADA <<<")

comparativo_bp = Blueprint("comparativo", __name__)

@comparativo_bp.route("/comparativo/<int:cotacao_id>")
def comparativo(cotacao_id):

    dados = buscar_comparativo(cotacao_id)

    return jsonify(dados)