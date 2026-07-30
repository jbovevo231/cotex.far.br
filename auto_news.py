import requests
from bs4 import BeautifulSoup
from database.connection import get_db
from models.conecta import salvar_post

URL = "https://site.cff.org.br/noticias"

EMAIL_OFICIAL = "jandersonpharma@gmail.com"


def buscar_usuario():

    db = get_db()

    return db.execute(
        """
        SELECT
            cnpj,
            nome
        FROM usuarios
        WHERE email = ?
        LIMIT 1
        """,
        (
            EMAIL_OFICIAL,
        )
    ).fetchone()


def buscar_noticia():

    resposta = requests.get(
        URL,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    for a in soup.find_all("a", href=True):

        href = a["href"].strip()
        titulo = a.get_text(strip=True)

        if "/noticia/" in href and titulo:

            return {
                "titulo": titulo,
                "link": href
            }

    return None


def ler_noticia(link):

    resposta = requests.get(
        link,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    texto = ""

    for p in soup.find_all("p"):

        conteudo = p.get_text(" ", strip=True)

        if len(conteudo) > 40:
            texto += conteudo + "\n\n"

    return texto.strip()


def noticia_ja_publicada(link):

    db = get_db()

    cursor = db.execute(
        """
        SELECT COUNT(*)
        FROM noticias_automaticas
        WHERE link = ?
        """,
        (link,)
    )

    return cursor.fetchone()[0] > 0


def salvar_noticia_publicada(titulo, link):

    db = get_db()

    db.execute(
        """
        INSERT INTO noticias_automaticas
        (
            titulo,
            link
        )
        VALUES
        (
            ?,
            ?
        )
        """,
        (
            titulo,
            link
        )
    )

    db.commit()


if __name__ == "__main__":

    usuario = buscar_usuario()

    if usuario is None:
        print("Usuário oficial não encontrado.")
        exit()

    cnpj = usuario[0]

    noticia = buscar_noticia()

    if noticia is None:
        print("Nenhuma notícia encontrada.")
        exit()

    if noticia_ja_publicada(noticia["link"]):
        print("Essa notícia já foi publicada.")
        exit()

    texto = ler_noticia(noticia["link"])

    print("=" * 80)
    print("PUBLICANDO NO CONECTA")
    print("=" * 80)

    postagem = f"""📰 CFF

{noticia["titulo"]}

{texto[:1200]}

🔗 Leia a matéria completa:
{noticia["link"]}
"""

    salvar_post(
        cnpj,
        "Cotex Conecta",
        postagem,
        None
    )

    salvar_noticia_publicada(
        noticia["titulo"],
        noticia["link"]
    )

    print("✅ Publicada no Conecta.")