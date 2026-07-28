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
    listar_posts_usuario,
    salvar_post,
    excluir_post
)


conecta_bp = Blueprint("conecta", __name__)


@conecta_bp.route("/conecta")
def conecta():

    print("ENTROU NA ROTA CONECTA")

    posts = listar_posts()

    print("NOME DA SESSÃO:", session.get("usuario_nome"))

    return render_template(
    "conecta.html",
    posts=posts,
    usuario_nome=session.get("usuario_nome"),
    seguidores=0,
    seguindo=0
)


@conecta_bp.route("/conecta/minhas-publicacoes")
def minhas_publicacoes():

    print("CNPJ DA SESSÃO:", session.get("usuario_cnpj"))

    posts = listar_posts_usuario(
        session.get("usuario_cnpj")
    )

    return render_template(
    "conecta.html",
    posts=posts,
    usuario_nome=session.get("usuario_nome"),
    seguidores=0,
    seguindo=0
)

@conecta_bp.route("/conecta/perfil/<cnpj>")
def perfil_usuario(cnpj):

    print("ABRINDO PERFIL DA FARMÁCIA:", cnpj)

    posts = listar_posts_usuario(cnpj)

    if posts:
        nome_usuario = posts[0][1]
    else:
        nome_usuario = "Farmácia"

    return render_template(
        "perfil_farmacia.html",
        posts=posts,
        usuario_nome=nome_usuario
    )


@conecta_bp.route("/conecta/excluir/<int:id_post>", methods=["POST"])
def excluir(id_post):

    print("EXCLUINDO POST:", id_post)

    cnpj_usuario = session.get("usuario_cnpj")

    excluir_post(
        id_post,
        cnpj_usuario
    )

    return redirect(
        request.referrer or url_for("conecta.conecta")
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