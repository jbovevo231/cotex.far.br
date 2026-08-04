print(">>> ROUTE ANALYTICS CARREGADA <<<")

from flask import Blueprint, render_template, session

analytics_bp = Blueprint(
    "analytics",
    __name__
)

@analytics_bp.route("/analytics")
def analytics():

    if "usuario_id" not in session:
        return render_template("login.html")

    return render_template("analytics.html")