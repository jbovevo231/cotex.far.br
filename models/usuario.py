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


def criar_usuario(nome, cpf, cnpj, telefone, email, senha):

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


def validar_login(cnpj, senha):

    db = get_db()

    cnpj = limpar_cnpj(cnpj)

    usuario = db.execute(
        """
        SELECT id, nome, cnpj, email, senha
        FROM usuarios
        WHERE cnpj = ?
        """,
        (cnpj,)
    ).fetchone()

    if usuario is None:
        return None

    senha_banco = usuario[4]

    if not check_password_hash(senha_banco, senha):
        print("SENHA INCORRETA")
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
        SET remember_token=?
        WHERE id=?
        """,
        (token, usuario_id)
    )

    db.commit()

    return token


def buscar_usuario_por_token(token):

    db = get_db()

    usuario = db.execute(
        """
        SELECT id, nome, cnpj, email
        FROM usuarios
        WHERE remember_token=?
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
        SET remember_token=NULL
        WHERE id=?
        """,
        (usuario_id,)
    )

    db.commit()


def buscar_usuario_por_cnpj_ou_email(identificacao):

    db = get_db()

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
   OR email = ?
   OR telefone = ?
        """,
        (
    limpar_cnpj(identificacao),
    identificacao,
    identificacao
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
            email,
            telefone
        FROM usuarios
        WHERE id=?
        """,
        (usuario_id,)
    ).fetchone()


    if usuario is None:
        return None


    return {
        "id": usuario[0],
        "nome": usuario[1],
        "cnpj": usuario[2],
        "email": usuario[3],
        "telefone": usuario[4]
    }