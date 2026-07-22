from flask import Blueprint, render_template

produtos_bp = Blueprint("produtos", __name__)

@produtos_bp.route("/produtos")
def produtos():
    return render_template("produtos.html")