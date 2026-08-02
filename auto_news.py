import requests
from bs4 import BeautifulSoup
from database.connection import get_db
from models.conecta import salvar_post

URL = "https://site.cff.org.br/noticias"

EMAIL_OFICIAL = "jandersonpharma@gmail.com"

URL_ANVISA = "https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa"

PALAVRAS_ANVISA = [

    "medicamento",
    "medicamentos",
    "novo medicamento",
    "registro",
    "registro sanitário",
    "indicação terapêutica",
    "farmacovigilância",
    "recall",
    "recolhimento",
    "lote",
    "suspensão",
    "interdição",
    "cancelamento de registro",
    "rdc",
    "controlado",
    "controlados",
    "sncr"

]

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


def buscar_noticia_cff():

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

def noticia_eh_medicamento(texto):

    texto = texto.lower()

    return any(
        palavra in texto
        for palavra in PALAVRAS_ANVISA
    )

def buscar_noticia_anvisa():

    resposta = requests.get(
        URL_ANVISA,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    for a in soup.find_all("a", href=True):

        titulo = a.get_text(" ", strip=True)
        href = a.get("href", "").strip()

        if not titulo:
            continue

        if href.startswith("/"):
            href = "https://www.gov.br" + href

        if not href.startswith("https://"):
            continue

        try:

            conteudo = ler_noticia(href)

            texto_completo = (
                titulo + " " + conteudo["texto"]
            )

        except Exception:
            continue

        if not noticia_eh_medicamento(texto_completo):
            continue

        return {
            "titulo": titulo,
            "link": href,
            "fonte": "ANVISA"
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

    imagem = None

    meta = soup.find("meta", property="og:image")

    if meta:
        imagem = meta.get("content")

    if not imagem:

        img = soup.find("img")

        if img:
            imagem = img.get("src")

    return {
        "texto": texto.strip(),
        "imagem": imagem
    }


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

    fontes = [

    buscar_noticia_cff,

    buscar_noticia_anvisa

]

    noticia = None

    for buscar in fontes:

            noticia = buscar()

            if noticia is None:
                continue

            if noticia_ja_publicada(noticia["link"]):
                continue

            break

    if noticia is None:

            print("Nenhuma notícia nova encontrada.")

            exit()

    if noticia.get("fonte") == "ANVISA":

        conteudo = ler_noticia(noticia["link"])

    else:

        conteudo = ler_noticia(noticia["link"])

    texto = conteudo["texto"]
    print("=" * 80)
    print(texto[:1500])
    print("=" * 80)
    imagem = conteudo["imagem"]

    print("=" * 80)
    print("PUBLICANDO NO CONECTA")
    print("=" * 80)

    fonte = noticia.get("fonte", "CFF")

    resumo = texto[:800]

    postagem = f"""[FONTE]{fonte}[/FONTE]

    [TITULO]{noticia["titulo"]}[/TITULO]

    [TEXTO]
    {resumo}
    [/TEXTO]

    [LINK]{noticia["link"]}[/LINK]
    """

    print(postagem)

    salvar_post(
        cnpj,
        "Cotex Conecta",
        postagem,
        imagem
    )

    salvar_noticia_publicada(
        noticia["titulo"],
        noticia["link"]
    )

    print("✅ Publicada no Conecta.")