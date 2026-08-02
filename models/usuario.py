from database.connection import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


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


def limpar_telefone(telefone):
    if not telefone:
        return ""

    return (
        str(telefone)
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
        .replace("+", "")
        .strip()
    )


def criar_usuario(nome, cpf, cnpj, telefone, email, senha):

    db = get_db()

    cnpj = limpar_cnpj(cnpj)
    telefone = limpar_telefone(telefone)
    email = email.strip().lower()
    cpf = cpf.strip()

    senha_hash = generate_password_hash(senha)

    existe = db.execute(
        """
        SELECT 
            cpf,
            cnpj,
            email,
            telefone
        FROM usuarios
        WHERE cpf = ?
           OR cnpj = ?
           OR LOWER(email) = LOWER(?)
           OR telefone = ?
        """,
        (
            cpf,
            cnpj,
            email,
            telefone
        )
    ).fetchone()


    if existe:

        if existe[0] == cpf:
            raise Exception(
                "CPF já cadastrado."
            )

        if existe[1] == cnpj:
            raise Exception(
                "CNPJ já cadastrado."
            )

        if existe[2].lower() == email:
            raise Exception(
                "E-mail já cadastrado."
            )

        if existe[3] == telefone:
            raise Exception(
                "WhatsApp já cadastrado."
            )


    db.execute(
        """
        INSERT INTO usuarios
        (
            nome,
            cpf,
            cnpj,
            telefone,
            email,
            senha
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            nome,
            cpf,
            cnpj,
            telefone,
            email,
            senha_hash
        )
    )

    db.commit()

    db.execute(
        """
        INSERT INTO usuarios
        (nome, cpf, cnpj, telefone, email, senha)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            nome,
            cpf,
            cnpj,
            telefone,
            email,
            senha_hash
        )
    )

    db.commit()


def validar_login(login, senha):

    print("VERSÃO NOVA DO USUARIO.PY")

    db = get_db()

    login = login.strip()

    login_cnpj = limpar_cnpj(login)
    login_telefone = limpar_telefone(login)
    login_email = login.lower()

    usuario = db.execute(
        """
        SELECT
            id,
            nome,
            cnpj,
            email,
            senha
        FROM usuarios
        WHERE cnpj = ?
           OR LOWER(email) = ?
           OR telefone = ?
        """,
        (
            login_cnpj,
            login_email,
            login_telefone
        )
    ).fetchone()

    if usuario is None:
        return None

    senha_banco = usuario[4]

    if not check_password_hash(senha_banco, senha):
        return None

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "cnpj": usuario[2],
        "email": usuario[3]
    }


# =====================================================
# REMEMBER ME
# =====================================================

def gerar_remember_token(usuario_id):

    token = secrets.token_hex(32)

    db = get_db()

    db.execute(
        """
        UPDATE usuarios
        SET remember_token = ?
        WHERE id = ?
        """,
        (token, usuario_id)
    )

    db.commit()

    return token


def buscar_usuario_por_token(token):

    db = get_db()

    usuario = db.execute(
        """
        SELECT
            id,
            nome,
            cnpj,
            email
        FROM usuarios
        WHERE remember_token = ?
        """,
        (token,)
    ).fetchone()

    if usuario is None:
        return None

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "cnpj": usuario[2],
        "email": usuario[3]
    }


def limpar_remember_token(usuario_id):

    db = get_db()

    db.execute(
        """
        UPDATE usuarios
        SET remember_token = NULL
        WHERE id = ?
        """,
        (usuario_id,)
    )

    db.commit()


def buscar_usuario_por_cnpj_ou_email(identificacao):

    db = get_db()

    identificacao = identificacao.strip()

    return db.execute(
        """
        SELECT
            id,
            nome,
            cnpj,
            telefone,
            email
        FROM usuarios
        WHERE cnpj = ?
           OR LOWER(email) = ?
           OR telefone = ?
        """,
        (
            limpar_cnpj(identificacao),
            identificacao.lower(),
            limpar_telefone(identificacao)
        )
    ).fetchone()


def buscar_usuario_por_id(usuario_id):

    db = get_db()

    usuario = db.execute(
        """
        SELECT
            id,
            nome,
            cnpj,
            telefone,
            email
        FROM usuarios
        WHERE id = ?
        """,
        (usuario_id,)
    ).fetchone()

    if usuario is None:
        return None

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "cnpj": usuario[2],
        "telefone": usuario[3],
        "email": usuario[4]
    }