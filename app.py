from flask import Flask

from config import Config

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.cotacao import cotacao_bp


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


app.config.from_object(Config)


app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(cotacao_bp)


@app.route("/")
def index():
    return "CotaFarma v2 funcionando"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000,
        debug=True
    )