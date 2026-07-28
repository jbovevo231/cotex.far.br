from flask import Flask, render_template, request, session

from config import Config

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.cotacao import cotacao_bp
from routes.conecta import conecta_bp
import routes.conecta
print(routes.conecta.__file__)
from routes.comparativo import comparativo_bp

from models.usuario import buscar_usuario_por_token

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = True

app.config.from_object(Config)


# =====================================
# RESTAURA A SESSÃO PELO COOKIE
# =====================================
@app.before_request
def restaurar_sessao():

    # Se já existe sessão, não faz nada
    if "usuario_id" in session:
        return

    # Lê o cookie
    token = request.cookies.get("remember_token")

    if not token:
        return

    # Procura o usuário pelo token
    usuario = buscar_usuario_por_token(token)

    if usuario is None:
        return

    # Recria a sessão
    session["usuario_id"] = usuario["id"]
    session["usuario_nome"] = usuario["nome"]
    session["usuario_email"] = usuario["email"]
    session["usuario_cnpj"] = usuario["cnpj"]


# ===========================
# REGISTRO DOS BLUEPRINTS
# ===========================

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(cotacao_bp)
app.register_blueprint(conecta_bp)
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