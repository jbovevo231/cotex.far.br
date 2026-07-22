from flask import Blueprint, render_template

distribuidoras_bp = Blueprint(
    "distribuidoras",
    __name__
)

@distribuidoras_bp.route("/distribuidoras")
def distribuidoras():
    return render_template("distribuidoras.html")