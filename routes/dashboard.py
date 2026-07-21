from flask import Blueprint, render_template, session

from services.dashboard_service import carregar_indicadores


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
def dashboard():

    cnpj = session.get(
        "usuario_cnpj"
    )


    indicadores = carregar_indicadores(
        cnpj
    )


    return render_template(
        "dashboard.html",
        indicadores=indicadores
    )