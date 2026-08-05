print(">>> ROUTE ANALYTICS CARREGADA <<<")

from flask import Blueprint, render_template, session, jsonify

from models.analytics import (
    buscar_cotacoes_realizadas,
    buscar_economia_gerada,
    buscar_taxa_resposta
)

analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route("/analytics")
def analytics():

    if "usuario_id" not in session:
        return render_template("login.html")

    return render_template("analytics.html")


@analytics_bp.route("/analytics/cotacoes-realizadas")
def analytics_cotacoes_realizadas():

    if "usuario_id" not in session:
        return jsonify([])

    return jsonify(buscar_cotacoes_realizadas())


@analytics_bp.route("/analytics/economia-gerada")
def analytics_economia_gerada():

    if "usuario_id" not in session:
        return jsonify([])

    return jsonify(buscar_economia_gerada())


print("FIM DO ARQUIVO ANALYTICS")

@analytics_bp.route("/analytics/taxa-resposta")
def analytics_taxa_resposta():

    if "usuario_id" not in session:
        return jsonify([])

    return jsonify(buscar_taxa_resposta())

print("FIM DO ARQUIVO ANALYTICS")