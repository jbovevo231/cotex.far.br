from flask import Flask, render_template

from config import Config

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.cotacao import cotacao_bp
from routes.produtos import produtos_bp
from routes.comparativo import comparativo_bp

app = Flask(__name__)

app.config.from_object(Config)

# ===========================
# REGISTRO DOS BLUEPRINTS
# ===========================

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(cotacao_bp)
app.register_blueprint(produtos_bp)
app.register_blueprint(comparativo_bp)


@app.route("/")
def inicio():
    return render_template("login.html")

print(app.url_map)
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=10000
    )