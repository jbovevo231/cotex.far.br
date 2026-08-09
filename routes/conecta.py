from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from database.connection import get_db

import cloudinary
import cloudinary.uploader
import cloudinary_config
import cloudinary.uploader

from models.conecta import (
    listar_posts,
    listar_posts_usuario,
    salvar_post,
    excluir_post,
    seguir_usuario,
    deixar_de_seguir,
    ja_segue,
    total_seguidores,
    total_seguindo
)


conecta_bp = Blueprint("conecta", __name__)


def buscar_perfil(cnpj):

    db = get_db()

    perfil = db.execute(
        """
        SELECT
            foto_perfil,
            foto_capa
        FROM usuarios
        WHERE cnpj = ?
        """,
        (
            cnpj,
        )
    ).fetchone()

    print("PERFIL BUSCADO:", perfil)

    return perfil

@conecta_bp.route("/conecta")
def conecta():

    cnpj = session.get("usuario_cnpj")

    posts = listar_posts()

    perfil = buscar_perfil(cnpj)

    foto_perfil = None
    foto_capa = None

    if perfil:
        foto_perfil = perfil[0]
        foto_capa = perfil[1]


    return render_template(
        "conecta.html",
        posts=posts,
        usuario_nome=session.get("usuario_nome"),
        seguidores=total_seguidores(cnpj),
        seguindo=total_seguindo(cnpj),
        perfil_cnpj=cnpj,
        foto_perfil=foto_perfil,
        foto_capa=foto_capa
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

@conecta_bp.route("/conecta/meu-perfil")
def meu_perfil():

    cnpj = session.get("usuario_cnpj")

    posts = listar_posts_usuario(cnpj)

    perfil = buscar_perfil(cnpj)


    return render_template(
        "perfil_farmacia.html",
        posts=posts,
        usuario_nome=session.get("usuario_nome"),
        meu_perfil=True,
        foto_perfil=perfil[1] if perfil else None,
        foto_capa=perfil[0] if perfil else None
    )

@conecta_bp.route("/conecta/perfil/<cnpj>")
def perfil_usuario(cnpj):

    posts = listar_posts_usuario(cnpj)

    perfil = buscar_perfil(cnpj)

    nome = "Farmácia"

    if posts:
        nome = posts[0][1]

    meu_cnpj = session.get("usuario_cnpj")

    print("===================================")
    print("MEU CNPJ:", meu_cnpj)
    print("CNPJ DO PERFIL:", cnpj)
    print("MEU PERFIL?:", meu_cnpj == cnpj)
    print("===================================")

    return render_template(
        "perfil_farmacia.html",
        posts=posts,
        usuario_nome=nome,
        foto_perfil=perfil[0] if perfil else None,
        foto_capa=perfil[1] if perfil else None,
        perfil_cnpj=cnpj,
        segue=ja_segue(meu_cnpj, cnpj),
        seguidores=total_seguidores(cnpj),
        seguindo=total_seguindo(cnpj),
        meu_perfil=(meu_cnpj == cnpj)
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

@conecta_bp.route("/conecta/editar-perfil", methods=["POST"])
def editar_perfil():

    cnpj = session.get("usuario_cnpj")

    foto_perfil = request.files.get("foto_perfil")
    foto_capa = request.files.get("foto_capa")


    print("========== TESTE FOTO ==========")
    print("FOTO PERFIL:", foto_perfil)
    print("FOTO CAPA:", foto_capa)
    print("=================================")


    perfil = None
    capa = None



    # ==========================
    # ENVIA FOTO DE PERFIL
    # ==========================

    if foto_perfil and foto_perfil.filename != "":

        print("ENVIANDO FOTO PERFIL PARA CLOUDINARY")

        resultado = cloudinary.uploader.upload(
            foto_perfil,
            folder="cotafarma/perfis"
        )

        perfil = resultado["secure_url"]

        print("URL FOTO PERFIL:", perfil)



    # ==========================
    # ENVIA FOTO DE CAPA
    # ==========================

    if foto_capa and foto_capa.filename != "":

        print("ENVIANDO FOTO CAPA PARA CLOUDINARY")

        resultado = cloudinary.uploader.upload(
            foto_capa,
            folder="cotafarma/capas"
        )

        capa = resultado["secure_url"]

        print("URL FOTO CAPA:", capa)



    # ==========================
    # SALVA NO BANCO
    # ==========================

    db = get_db()


    if perfil:

        db.execute(
            """
            UPDATE usuarios
            SET foto_perfil = ?
            WHERE cnpj = ?
            """,
            (
                perfil,
                cnpj
            )
        )



    if capa:

        db.execute(
            """
            UPDATE usuarios
            SET foto_capa = ?
            WHERE cnpj = ?
            """,
            (
                capa,
                cnpj
            )
        )



    db.commit()



    return redirect(
        url_for("conecta.conecta")
    )

@conecta_bp.route("/conecta/seguir/<cnpj>", methods=["POST"])
def alternar_seguir(cnpj):

    meu_cnpj = session.get("usuario_cnpj")

    # impede seguir a si mesmo
    if meu_cnpj == cnpj:
        return redirect(
            url_for("conecta.perfil_usuario", cnpj=cnpj)
        )

    if ja_segue(meu_cnpj, cnpj):

        deixar_de_seguir(
            meu_cnpj,
            cnpj
        )

    else:

        seguir_usuario(
            meu_cnpj,
            cnpj
        )

    return redirect(
        url_for("conecta.perfil_usuario", cnpj=cnpj)
    )

@conecta_bp.route("/conecta/publicar", methods=["POST"])
def publicar():

    texto = request.form.get("texto", "").strip()

    foto = request.files.get("foto")

    # Tipo da publicação
    tipo = request.form.get("tipo", "normal")

    nome_arquivo = None

    try:

        # ==========================
        # VALIDAÇÃO
        # ==========================

        if not texto and not foto:
            return redirect(
                url_for("conecta.conecta")
            )


        # ==========================
        # ENVIA FOTO
        # ==========================

        if foto and foto.filename:

            resultado = cloudinary.uploader.upload(
                foto,
                folder="cotafarma/conecta",
                resource_type="image"
            )

            nome_arquivo = resultado["secure_url"]

            print("Imagem enviada:")
            print(nome_arquivo)


        # ==========================
        # SALVA PUBLICAÇÃO
        # ==========================

        tipo = request.form.get("tipo", "normal")

        print("TIPO DA PUBLICAÇÃO:", tipo)


        salvar_post(
            session.get("usuario_cnpj"),
            session.get("usuario_nome") or "Usuário",
            texto,
            nome_arquivo,
            tipo
        )


        print("================================")
        print("PUBLICAÇÃO SALVA")
        print("CNPJ:", session.get("usuario_cnpj"))
        print("USUÁRIO:", session.get("usuario_nome"))
        print("TIPO:", tipo)
        print("================================")


        return redirect(
            url_for("conecta.conecta")
        )


    except Exception as e:

        print("ERRO AO PUBLICAR:")
        print(repr(e))

        raise