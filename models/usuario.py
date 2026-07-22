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

    existe = db.execute(
        "SELECT id FROM usuarios WHERE cnpj = ?",
        (cnpj,)
    ).fetchone()

    if existe:
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
        WHERE cnpj = ?
        """,
        (cnpj,)
    ).fetchone()

    if usuario is None:
        print("CNPJ NÃO ENCONTRADO")
        return None

    senha_banco = usuario[3]

    if not check_password_hash(senha_banco, senha):
        print("SENHA INCORRETA")
        return None

    print("LOGIN APROVADO")

    return {
        "id": usuario[0],
        "cnpj": usuario[1],
        "email": usuario[2]
    }