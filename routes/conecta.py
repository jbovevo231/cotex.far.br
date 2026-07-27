from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import os
import uuid

from models.conecta import (
    listar_posts,
    salvar_post
)

conecta_bp = Blueprint("conecta", __name__)


@conecta_bp.route("/conecta")
def conecta():

    posts = listar_posts()
    print(posts)

    return render_template(
        "conecta.html",
        posts=posts
    )


@conecta_bp.route("/conecta/publicar", methods=["POST"])
def publicar():

    texto = request.form.get("texto", "").strip()

    foto = request.files.get("foto")

    nome_arquivo = None

    try:

        if foto and foto.filename:

            pasta = "static/uploads/conecta"
            os.makedirs(pasta, exist_ok=True)

            extensao = os.path.splitext(foto.filename)[1]

            nome_arquivo = f"{uuid.uuid4().hex}{extensao}"

            caminho = os.path.join(
                pasta,
                nome_arquivo
            )

            print("SALVANDO EM:", caminho)

            foto.save(caminho)

            print("FOTO SALVA COM SUCESSO")

        print("SESSÃO:", dict(session))
        print("NOME:", session.get("usuario_nome"))

        salvar_post(
            session.get("usuario_cnpj"),
            session.get("usuario_nome", "Usuário"),
            texto,
            nome_arquivo
        )

        return redirect(url_for("conecta.conecta"))

    except Exception as e:

        print("ERRO NA ROTA PUBLICAR:", repr(e))

        raise
