from flask import Blueprint, render_template

cotacao_bp = Blueprint("cotacao", __name__)

@cotacao_bp.route("/cotacoes")
def cotacoes():
    return render_template("cotacoes.html")