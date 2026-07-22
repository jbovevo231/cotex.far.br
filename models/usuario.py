from database.connection import get_db
from werkzeug.security import generate_password_hash, check_password_hash


def limpar_cnpj(cnpj):
    if not cnpj:
        return ""

    return (
        str(cnpj)
        .replace(".", "")
        .replace("/", "")
        .replace("-", "")
        .replace(" ", "")
        .strip()
    )


def criar_usuario(nome, cpf, cnpj, email, senha):

    db = get_db()

    cnpj = limpar_cnpj(cnpj)

    senha_hash = generate_password_hash(senha)

    print("SENHA ORIGINAL:", senha)
    print("HASH GERADO:", senha_hash)
    print("CNPJ salvo:", cnpj)


    existe = db.execute(
        "SELECT id FROM usuarios WHERE cnpj=?",
        (cnpj,)
    )

    if existe.fetchone():
        raise Exception("CNPJ já cadastrado")


    db.execute(
        """
        INSERT INTO usuarios
        (nome, cpf, cnpj, email, senha)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            nome,
            cpf,
            cnpj,
            email,
            senha_hash
        )
    )

    db.commit()



def validar_login(cnpj, senha):

    db = get_db()

    cnpj = limpar_cnpj(cnpj)

    usuario = db.execute(
        """
        SELECT id, cnpj, email, senha
        FROM usuarios
        WHERE cnpj=?
        """,
        (cnpj,)
    ).fetchone()


    if not usuario:
        print("CNPJ NÃO ENCONTRADO")
        return None


    print("USUARIO:", usuario)

    senha_banco = usuario[3]

    print("SENHA DIGITADA:", senha)
    print("SENHA BANCO:", senha_banco)


    resultado = check_password_hash(
        senha_banco,
        senha
    )


    print("RESULTADO SENHA:", resultado)


    if resultado:

        print("LOGIN APROVADO")

        return {
            "id": usuario[0],
            "cnpj": usuario[1],
            "email": usuario[2]
        }


    print("LOGIN NEGADO")

    return None