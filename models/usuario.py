from database.connection import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


# =========================================================
# LIMPAR CNPJ
# =========================================================

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


# =========================================================
# LIMPAR TELEFONE
# =========================================================

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


# =========================================================
# CRIAR USUÁRIO
# =========================================================

def criar_usuario(
    nome,
    cpf,
    cnpj,
    telefone,
    email,
    senha
):

    db = get_db()


    cnpj = limpar_cnpj(cnpj)

    telefone = limpar_telefone(telefone)

    email = email.strip().lower()

    cpf = cpf.strip()


    senha_hash = generate_password_hash(
        senha
    )


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


# =========================================================
# VALIDAR LOGIN
# =========================================================

def validar_login(
    login,
    senha
):

    login = login.strip()

    login_cnpj = limpar_cnpj(
        login
    )

    login_telefone = limpar_telefone(
        login
    )

    login_email = login.lower()

    print("LOGIN: antes do get_db()", flush=True)

    db = get_db()

    print("LOGIN: depois do get_db()", flush=True)

    print("LOGIN: antes do EXECUTE", flush=True)

    try:

        resultado = db.execute(
            "SELECT 1",
            timeout=10
        )

        print("LOGIN: depois do EXECUTE", flush=True)

    except Exception as e:

        print(
            "LOGIN: ERRO NO EXECUTE:",
            repr(e),
            flush=True
        )

        return None

    print("LOGIN: antes do FETCHONE", flush=True)

    usuario = resultado.fetchone()

    print("LOGIN: depois do FETCHONE", flush=True)

    return None
# =========================================================
# REMEMBER ME
# =========================================================

def gerar_remember_token(
    usuario_id
):

    token = secrets.token_hex(32)


    db = get_db()


    db.execute(
        """
        UPDATE usuarios
        SET remember_token = ?
        WHERE id = ?
        """,
        (
            token,
            usuario_id
        )
    )


    db.commit()


    return token


# =========================================================
# BUSCAR USUÁRIO POR TOKEN
# =========================================================

def buscar_usuario_por_token(
    token
):

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
        (
            token,
        )
    ).fetchone()


    if usuario is None:

        return None


    return {
        "id": usuario[0],
        "nome": usuario[1],
        "cnpj": usuario[2],
        "email": usuario[3]
    }


# =========================================================
# LIMPAR REMEMBER TOKEN
# =========================================================

def limpar_remember_token(
    usuario_id
):

    db = get_db()


    db.execute(
        """
        UPDATE usuarios
        SET remember_token = NULL
        WHERE id = ?
        """,
        (
            usuario_id,
        )
    )


    db.commit()


# =========================================================
# BUSCAR POR CNPJ / E-MAIL / TELEFONE
# =========================================================

def buscar_usuario_por_cnpj_ou_email(
    identificacao
):

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
            limpar_cnpj(
                identificacao
            ),
            identificacao.lower(),
            limpar_telefone(
                identificacao
            )
        )
    ).fetchone()


# =========================================================
# BUSCAR USUÁRIO POR ID
# =========================================================

def buscar_usuario_por_id(
    usuario_id
):

    db = get_db()

    usuario = db.execute(
        """
        SELECT
            id,
            nome,
            cnpj,
            telefone,
            email,
            plano,
            periodo_teste,
            trial_fim
        FROM usuarios
        WHERE id = ?
        """,
        (
            usuario_id,
        )
    ).fetchone()

    if usuario is None:

        return None

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "cnpj": usuario[2],
        "telefone": usuario[3],
        "email": usuario[4],
        "plano": usuario[5] if usuario[5] else "teste",
        "periodo_teste": usuario[6],
        "trial_fim": usuario[7]
    }

# =========================================================
# ADMIN - LISTAR USUÁRIOS
# =========================================================

def listar_usuarios_admin():

    db = get_db()

    usuarios = db.execute(
        """
        SELECT
            id,
            nome,
            cpf,
            cnpj,
            telefone,
            email,
            plano,
            periodo_teste,
            trial_fim,
            status
        FROM usuarios
        ORDER BY id DESC
        """
    ).fetchall()

    return usuarios


# =========================================================
# ADMIN - CONTADORES
# =========================================================

def contar_usuarios_admin():

    db = get_db()

    total = db.execute(
        """
        SELECT COUNT(*)
        FROM usuarios
        """
    ).fetchone()[0]

    ativos = db.execute(
        """
        SELECT COUNT(*)
        FROM usuarios
        WHERE status = 'ativo'
        """
    ).fetchone()[0]

    desativados = db.execute(
        """
        SELECT COUNT(*)
        FROM usuarios
        WHERE status = 'desativado'
        """
    ).fetchone()[0]

    return {
        "total": total,
        "ativos": ativos,
        "desativados": desativados
    }


# =========================================================
# ADMIN - ALTERAR STATUS
# =========================================================

def alterar_status_usuario(usuario_id, status):

    if status not in ("ativo", "desativado"):
        raise ValueError("Status inválido.")

    db = get_db()

    db.execute(
        """
        UPDATE usuarios
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            usuario_id
        )
    )

    db.commit()