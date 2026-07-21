from database.connection import get_db
from werkzeug.security import generate_password_hash, check_password_hash


def limpar_cnpj(cnpj):
    return (
        cnpj
        .replace(".", "")
        .replace("/", "")
        .replace("-", "")
        .strip()
    )


def criar_usuario(nome, cpf, cnpj, email, senha):

    db = get_db()

    cnpj = limpar_cnpj(cnpj)

    existe = db.execute(
        "SELECT id FROM usuarios WHERE cnpj=?",
        (cnpj,)
    )

    if existe.fetchone():
        raise Exception("CNPJ já cadastrado")


    senha_hash = generate_password_hash(senha)


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

    import hashlib

    db = get_db()

    cnpj = limpar_cnpj(cnpj)


    resultado = db.execute(
        """
        SELECT *
        FROM usuarios
        WHERE cnpj=?
        """,
        (cnpj,)
    )


    usuario = resultado.fetchone()


    if not usuario:
        return None


    senha_banco = usuario[3]


    # tenta senha normal
    if senha_banco == senha:
        return {
            "id": usuario[0],
            "cnpj": usuario[1],
            "email": usuario[2]
        }


    # tenta senha com SHA256 (sistema antigo)
    senha_hash = hashlib.sha256(
        senha.encode()
    ).hexdigest()


    if senha_hash == senha_banco:

        return {
            "id": usuario[0],
            "cnpj": usuario[1],
            "email": usuario[2]
        }


    print("Senha inválida")
    print("Digitada:", senha)
    print("SHA256:", senha_hash)
    print("Banco:", senha_banco)


    return None