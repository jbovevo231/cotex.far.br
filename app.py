from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()


import os
import cloudinary


# ===========================
# CONFIG CLOUDINARY
# ===========================

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


print("CLOUD NAME:", os.getenv("CLOUDINARY_CLOUD_NAME"))
print("API KEY:", os.getenv("CLOUDINARY_API_KEY"))
print("API SECRET:", os.getenv("CLOUDINARY_API_SECRET"))



from flask import Flask, render_template, request, session

from config import Config

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.cotacao import cotacao_bp
from routes.conecta import conecta_bp
from routes.analytics import analytics_bp

print("IMPORT DO ANALYTICS OK")

import routes.conecta

print(routes.conecta.__file__)

from routes.comparativo import comparativo_bp

from models.usuario import buscar_usuario_por_token

from database.connection import get_db



app = Flask(__name__)

# =====================================
# VERIFICAR ESTRUTURA DA TABELA USUARIOS
# =====================================

try:

    db = get_db()

    colunas = db.execute(
        "PRAGMA table_info(usuarios)"
    ).fetchall()

    print("===================================")
    print("COLUNAS DA TABELA USUARIOS:")
    print("===================================")

    for coluna in colunas:
        print(coluna)

    print("===================================")

except Exception as e:

    print("ERRO AO VERIFICAR USUARIOS:")
    print(e)


app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = True


app.config.from_object(Config)

# =====================================
# RESTAURA A SESSÃO PELO COOKIE
# =====================================
@app.before_request
def restaurar_sessao():

    print(">>> BEFORE REQUEST:", request.path)

    if "usuario_id" in session:
        print(">>> JÁ POSSUI SESSÃO")
        return

    token = request.cookies.get("remember_token")

    print(">>> TOKEN:", bool(token))

    if not token:
        return

    print(">>> BUSCANDO USUARIO PELO TOKEN")

    usuario = buscar_usuario_por_token(token)

    print(">>> USUARIO ENCONTRADO:", usuario is not None)

    if usuario is None:
        return

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

print("ANALYTICS_BP:", analytics_bp)
app.register_blueprint(analytics_bp)

print("BLUEPRINT ANALYTICS REGISTRADO")


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