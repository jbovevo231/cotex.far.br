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
            senha,
            plano,
            premium_ate
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

    plano = usuario[5]
    premium_ate = usuario[6]

    if plano == "premium" and premium_ate:

        try:

            vencimento = datetime.strptime(
                premium_ate,
                "%Y-%m-%d %H:%M:%S"
            )

            if datetime.now() > vencimento:

                db.execute(
                    """
                    UPDATE usuarios
                    SET
                        plano = 'gratuito',
                        premium_ate = NULL
                    WHERE id = ?
                    """,
                    (usuario[0],)
                )

                db.commit()

                plano = "gratuito"

        except Exception:
            pass

    if not check_password_hash(senha_banco, senha):
        return None

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "cnpj": usuario[2],
        "email": usuario[3],
        "plano": plano
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

from datetime import datetime, timedelta
from database.connection import get_db


def ativar_teste_gratis(cnpj):
    conn = get_db()
    cursor = conn.cursor()

    premium_ate = (
    datetime.now() + timedelta(days=14)
).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE usuarios
        SET
            plano = 'premium',
            premium_ate = ?,
            periodo_teste = TRUE
        WHERE cnpj = ?
    """, (premium_ate, cnpj))

    conn.commit()

def buscar_usuario_por_cnpj(cnpj):

    db = get_db()

    usuario = db.execute(
        """
        SELECT
            id,
            nome,
            cnpj,
            plano,
            premium_ate,
            periodo_teste
        FROM usuarios
        WHERE cnpj = ?
        """,
        (limpar_cnpj(cnpj),)
    ).fetchone()

    if usuario is None:
        return None

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "cnpj": usuario[2],
        "plano": usuario[3],
        "premium_ate": usuario[4],
        "periodo_teste": usuario[5]
    }