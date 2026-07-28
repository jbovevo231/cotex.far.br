from database.connection import get_db



def listar_posts():

    db = get_db()

    posts = db.execute(
        """
        SELECT
            id,
            usuario,
            texto,
            imagem,
            data_postagem,
            cnpj
        FROM conecta_posts
        ORDER BY id DESC
        """
    ).fetchall()

    return posts




def listar_posts_usuario(cnpj):

    print("CNPJ RECEBIDO:", cnpj)

    db = get_db()

    posts = db.execute(
        """
        SELECT
            id,
            usuario,
            texto,
            imagem,
            data_postagem,
            cnpj
        FROM conecta_posts
        WHERE cnpj = ?
        ORDER BY id DESC
        """,
        (
            cnpj,
        )
    ).fetchall()


    print("POSTS ENCONTRADOS:", posts)

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