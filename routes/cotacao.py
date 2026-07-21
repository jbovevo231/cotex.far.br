from flask import Blueprint


cotacao_bp = Blueprint(
    "cotacao",
    __name__
)


@cotacao_bp.route("/nova-cotacao")
def nova_cotacao():

    return "Nova cotação CotaFarma v2"