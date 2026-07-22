from flask import Blueprint, render_template

configuracoes_bp = Blueprint(
    "configuracoes",
    __name__
)

@configuracoes_bp.route("/configuracoes")
def configuracoes():
    return render_template("configuracoes.html")