from flask import Flask, render_template

from config import Config

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.cotacao import cotacao_bp


app = Flask(__name__)

app.config.from_object(Config)


# registra rotas
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(cotacao_bp)


@app.route("/")
def inicio():

    return render_template("login.html")


if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=10000
    )