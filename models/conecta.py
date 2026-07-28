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
            data_postagem
        FROM conecta_posts
        ORDER BY id DESC
        """
    ).fetchall()

    return posts


def listar_posts_usuario(cnpj):

    db = get_db()

    posts = db.execute(
        """
        SELECT
            id,
            usuario,
            texto,
            imagem,
            data_postagem
        FROM conecta_posts
        WHERE cnpj = ?
        ORDER BY id DESC
        """,
        (cnpj,)
    ).fetchall()

    return posts


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
        (?, ?, ?, ?)
        """,
        (
            cnpj,
            usuario,
            texto,
            imagem
        )
    )

    db.commit()