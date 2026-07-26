from flask import Blueprint, render_template

conecta_bp = Blueprint("conecta", __name__)

@conecta_bp.route("/conecta")
def conecta():
    return render_template("conecta.html")