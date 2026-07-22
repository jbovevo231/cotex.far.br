from flask import Blueprint, render_template

inteligencia_bp = Blueprint(
    "inteligencia",
    __name__
)

@inteligencia_bp.route("/inteligencia")
def inteligencia():
    return render_template("inteligencia.html")