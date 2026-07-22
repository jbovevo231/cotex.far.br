from flask import Blueprint, render_template

relatorios_bp = Blueprint(
    "relatorios",
    __name__
)

@relatorios_bp.route("/relatorios")
def relatorios():
    return render_template("relatorios.html")