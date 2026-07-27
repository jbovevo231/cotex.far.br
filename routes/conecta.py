from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import cloudinary
import cloudinary.uploader
import cloudinary_config

from models.conecta import (
    listar_posts,
    salvar_post
)

conecta_bp = Blueprint("conecta", __name__)



@conecta_bp.route("/conecta")
def conecta():

    print("ENTROU NA ROTA CONECTA")

    posts = listar_posts()

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

            resultado = cloudinary.uploader.upload(
                foto,
                folder="cotafarma/conecta",
                resource_type="image"
            )

            nome_arquivo = resultado["secure_url"]

            print("Imagem enviada:")
            print(nome_arquivo)

        salvar_post(
            session.get("usuario_cnpj"),
            session.get("usuario_nome") or "Usuário",
            texto,
            nome_arquivo
        )

        return redirect(
            url_for("conecta.conecta")
        )

    except Exception as e:

        print("ERRO CLOUDINARY:")
        print(repr(e))

        raise