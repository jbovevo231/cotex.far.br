from database.connection import get_db



def listar_posts():

    db = get_db()

    posts = db.execute(
        """
        SELECT
            conecta_posts.id,
            conecta_posts.usuario,
            conecta_posts.texto,
            conecta_posts.imagem,
            conecta_posts.data_postagem,
            conecta_posts.cnpj,
            usuarios.foto_perfil
        FROM conecta_posts
        LEFT JOIN usuarios
        ON conecta_posts.cnpj = usuarios.cnpj
        ORDER BY conecta_posts.id DESC
        """
    ).fetchall()


    print("POSTS COM FOTO:")
    for p in posts:
        print(p)


    return posts




def listar_posts_usuario(cnpj):

    db = get_db()

    posts = db.execute(
        """
        SELECT
            conecta_posts.id,
            conecta_posts.usuario,
            conecta_posts.texto,
            conecta_posts.imagem,
            conecta_posts.data_postagem,
            conecta_posts.cnpj,
            usuarios.foto_perfil

        FROM conecta_posts

        LEFT JOIN usuarios
        ON conecta_posts.cnpj = usuarios.cnpj

        WHERE conecta_posts.cnpj = ?

        ORDER BY conecta_posts.id DESC
        """,
        (
            cnpj,
        )
    ).fetchall()

    return posts



def excluir_post(id_post, cnpj):

    db = get_db()

    db.execute(
        """
        DELETE FROM conecta_posts
        WHERE id = ?
        AND cnpj = ?
        """,
        (
            id_post,
            cnpj
        )
    )

    db.commit()




def salvar_post(cnpj, usuario, texto, imagem):

    db = get_db()

    db.execute(
        """
        INSERT INTO conecta_posts
        (
            cnpj,
            usuario,
            texto,
            imagem
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?
        )
        """,
        (
            cnpj,
            usuario,
            texto,
            imagem
        )
    )

    db.commit()




def buscar_perfil(cnpj):

    db = get_db()

    perfil = db.execute(
        """
        SELECT
            foto_capa,
            foto_perfil
        FROM usuarios
        WHERE cnpj = ?
        """,
        (cnpj,)
    ).fetchone()


    print("PERFIL BUSCADO:", perfil)

    return perfil