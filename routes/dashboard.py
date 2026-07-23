from flask import Blueprint, render_template, session

from services.dashboard_service import (
    carregar_indicadores,
    carregar_ultimas_cotacoes
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
def dashboard():

    cnpj = session.get("usuario_cnpj")

    indicadores = carregar_indicadores(cnpj)

    ultimas_cotacoes = carregar_ultimas_cotacoes(cnpj)

    return render_template(
        "dashboard.html",
        indicadores=indicadores,
        ultimas_cotacoes=ultimas_cotacoes
    )