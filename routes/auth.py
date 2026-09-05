from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    session,
    make_response,
    jsonify
)

from models.usuario import (
    criar_usuario,
    validar_login,
    gerar_remember_token,
    limpar_remember_token,
    buscar_usuario_por_cnpj_ou_email
)

from database.connection import get_db

from werkzeug.security import generate_password_hash

import secrets
import hashlib
import hmac
import smtplib
import os
import time

from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# =========================================================
# BLUEPRINT
# =========================================================

auth_bp = Blueprint(
    "auth",
    __name__
)


# =========================================================
# CONFIGURAÇÃO DO E-MAIL
# =========================================================

EMAIL_REMETENTE = os.getenv("COTEX_EMAIL_REMETENTE")
EMAIL_SENHA_APP = os.getenv("COTEX_EMAIL_SENHA_APP")

# =========================================================
# ENVIO DE E-MAIL
# =========================================================

def enviar_email(destino, assunto, corpo):

    if not EMAIL_REMETENTE or not EMAIL_SENHA_APP:
        raise RuntimeError(
            "E-mail não configurado. "
            "Configure COTEX_EMAIL_REMETENTE "
            "e COTEX_EMAIL_SENHA_APP."
        )

    mensagem = MIMEMultipart()

    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = destino
    mensagem["Subject"] = assunto

    mensagem.attach(
        MIMEText(
            corpo,
            "plain",
            "utf-8"
        )
    )

    servidor = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        timeout=20
    )

    try:
        servidor.login(
            EMAIL_REMETENTE,
            EMAIL_SENHA_APP
        )

        servidor.sendmail(
            EMAIL_REMETENTE,
            destino,
            mensagem.as_string()
        )

    finally:
        servidor.quit()


# =========================================================
# ENVIAR CÓDIGO DE CONFIRMAÇÃO DE E-MAIL
# =========================================================

def enviar_codigo_email(destino, codigo):

    assunto = "Confirme seu novo e-mail - CotaUP"

    corpo = f"""
Olá! Como vai?

Recebemos uma solicitação para alterar o e-mail da sua conta CotaUP.

Seu código de confirmação é:

{codigo}

Se você não solicitou essa alteração, ignore este e-mail.

Equipe CotaUP
"""

    enviar_email(destino, assunto, corpo)

# =========================================================
# CADASTRO
# =========================================================

@auth_bp.route(
    "/cadastro",
    methods=["POST"]
)
def cadastro():

    nome = request.form["nome"]
    cpf = request.form["cpf"]
    cnpj = request.form["cnpj"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    senha = request.form["senha"]
    confirmar = request.form["confirmar"]


    if senha != confirmar:

        return jsonify({
            "erro": "As senhas não conferem."
        })


    try:

        criar_usuario(
            nome,
            cpf,
            cnpj,
            telefone,
            email,
            senha
        )


    except Exception as e:

        return jsonify({
            "erro": str(e)
        })


    return jsonify({
        "sucesso": True
    })


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    login = request.form["login"].strip()
    senha = request.form["senha"]


    usuario = validar_login(
        login,
        senha
    )


    if usuario:

        session["usuario_id"] = usuario["id"]

        session["usuario_nome"] = usuario["nome"]

        session["usuario_email"] = usuario["email"]

        session["usuario_cnpj"] = usuario["cnpj"]


        token = gerar_remember_token(
            usuario["id"]
        )


        resposta = make_response(
            redirect(
                url_for(
                    "dashboard.dashboard"
                )
            )
        )


        resposta.set_cookie(
            "remember_token",
            token,
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            secure=True,
            samesite="Lax"
        )


        return resposta


    return "CNPJ, e-mail, WhatsApp ou senha inválidos."


# =========================================================
# RECUPERAR SENHA
# =========================================================

@auth_bp.route(
    "/recuperar-senha",
    methods=["POST"]
)
def recuperar_senha():

    identificacao = request.form.get(
        "identificacao",
        ""
    ).strip()


    if not identificacao:

        return jsonify({
            "sucesso": False,
            "erro": "Informe seu e-mail ou CNPJ."
        }), 400


    usuario = buscar_usuario_por_cnpj_ou_email(
        identificacao
    )


    if usuario is None:

        return jsonify({
            "sucesso": False,
            "erro": "Usuário não encontrado."
        }), 404


    # -----------------------------------------------------
    # SEU usuario.py RETORNA:
    #
    # id
    # nome
    # cnpj
    # telefone
    # email
    #
    # Portanto o e-mail está em usuario[4]
    # -----------------------------------------------------

    email = usuario[4]


    if not email:

        return jsonify({
            "sucesso": False,
            "erro": (
                "Esta conta não possui "
                "um e-mail cadastrado."
            )
        }), 400


    # -----------------------------------------------------
    # GERA CÓDIGO DE 6 DÍGITOS
    # -----------------------------------------------------

    codigo = f"{secrets.randbelow(1000000):06d}"


    # -----------------------------------------------------
    # HASH DO CÓDIGO
    # -----------------------------------------------------

    codigo_hash = hashlib.sha256(
        codigo.encode("utf-8")
    ).hexdigest()


    # -----------------------------------------------------
    # SALVA TEMPORARIAMENTE NA SESSÃO
    #
    # VALIDADE: 10 MINUTOS
    # -----------------------------------------------------

    session["recuperacao_usuario_id"] = usuario[0]

    session["recuperacao_codigo_hash"] = codigo_hash

    session["recuperacao_expira"] = (
        time.time() + 600
    )

    session["recuperacao_verificada"] = False


    # -----------------------------------------------------
    # E-MAIL
    # -----------------------------------------------------

    assunto = (
        "Código de recuperação de senha - CotaX"
    )


    corpo = f"""
Olá, {usuario[1]}.

Recebemos uma solicitação para recuperar
a senha da sua conta CotaX.

Seu código de recuperação é:

{codigo}

Este código é válido por 10 minutos.

Se você não solicitou a recuperação da senha,
ignore este e-mail.

Atenciosamente,

Equipe CotaX
"""


    try:

        enviar_email(
            email,
            assunto,
            corpo
        )


    except Exception as e:

        print(
            "ERRO AO ENVIAR E-MAIL:",
            e
        )


        # Apaga a recuperação temporária

        session.pop(
            "recuperacao_usuario_id",
            None
        )

        session.pop(
            "recuperacao_codigo_hash",
            None
        )

        session.pop(
            "recuperacao_expira",
            None
        )

        session.pop(
            "recuperacao_verificada",
            None
        )


        return jsonify({
            "sucesso": False,
            "erro": (
                "Não foi possível enviar o código "
                "para o seu e-mail. "
                "Verifique a configuração do e-mail."
            )
        }), 500


    return jsonify({
        "sucesso": True,
        "mensagem": (
            "Código enviado para seu e-mail."
        )
    })


# =========================================================
# VERIFICAR CÓDIGO
# =========================================================

@auth_bp.route(
    "/verificar-codigo-recuperacao",
    methods=["POST"]
)
def verificar_codigo_recuperacao():

    codigo = request.form.get(
        "codigo",
        ""
    ).strip()


    if not codigo:

        return jsonify({
            "sucesso": False,
            "erro": "Digite o código recebido por e-mail."
        }), 400


    codigo_hash_salvo = session.get(
        "recuperacao_codigo_hash"
    )

    expiracao = session.get(
        "recuperacao_expira"
    )

    usuario_id = session.get(
        "recuperacao_usuario_id"
    )


    if (
        not codigo_hash_salvo
        or not expiracao
        or not usuario_id
    ):

        return jsonify({
            "sucesso": False,
            "erro": (
                "A recuperação não está mais válida. "
                "Solicite um novo código."
            )
        }), 400


    # -----------------------------------------------------
    # VERIFICA EXPIRAÇÃO
    # -----------------------------------------------------

    if time.time() > float(expiracao):

        session.pop(
            "recuperacao_codigo_hash",
            None
        )

        session.pop(
            "recuperacao_expira",
            None
        )

        session.pop(
            "recuperacao_verificada",
            None
        )


        return jsonify({
            "sucesso": False,
            "erro": (
                "O código expirou. "
                "Solicite um novo código."
            )
        }), 400


    # -----------------------------------------------------
    # HASH DO CÓDIGO DIGITADO
    # -----------------------------------------------------

    codigo_hash = hashlib.sha256(
        codigo.encode("utf-8")
    ).hexdigest()


    # -----------------------------------------------------
    # COMPARAÇÃO SEGURA
    # -----------------------------------------------------

    if not hmac.compare_digest(
        codigo_hash,
        codigo_hash_salvo
    ):

        return jsonify({
            "sucesso": False,
            "erro": "Código incorreto."
        }), 400


    # -----------------------------------------------------
    # CÓDIGO CORRETO
    # -----------------------------------------------------

    session["recuperacao_verificada"] = True


    return jsonify({
        "sucesso": True,
        "mensagem": (
            "Código confirmado. "
            "Agora crie sua nova senha."
        )
    })


# =========================================================
# REDEFINIR SENHA
# =========================================================

@auth_bp.route(
    "/redefinir-senha",
    methods=["POST"]
)
def redefinir_senha():

    usuario_id = session.get(
        "recuperacao_usuario_id"
    )

    verificada = session.get(
        "recuperacao_verificada"
    )

    expiracao = session.get(
        "recuperacao_expira"
    )


    if not usuario_id or not verificada:

        return jsonify({
            "sucesso": False,
            "erro": (
                "A recuperação não foi autorizada."
            )
        }), 403


    # -----------------------------------------------------
    # VERIFICA EXPIRAÇÃO
    # -----------------------------------------------------

    if (
        not expiracao
        or time.time() > float(expiracao)
    ):

        session.pop(
            "recuperacao_usuario_id",
            None
        )

        session.pop(
            "recuperacao_codigo_hash",
            None
        )

        session.pop(
            "recuperacao_expira",
            None
        )

        session.pop(
            "recuperacao_verificada",
            None
        )


        return jsonify({
            "sucesso": False,
            "erro": (
                "A recuperação expirou. "
                "Solicite um novo código."
            )
        }), 400


    # -----------------------------------------------------
    # NOVA SENHA
    # -----------------------------------------------------

    nova_senha = request.form.get(
        "senha",
        ""
    )


    confirmar = request.form.get(
        "confirmar",
        ""
    )


    if len(nova_senha) < 6:

        return jsonify({
            "sucesso": False,
            "erro": (
                "A nova senha deve ter "
                "pelo menos 6 caracteres."
            )
        }), 400


    if nova_senha != confirmar:

        return jsonify({
            "sucesso": False,
            "erro": (
                "As senhas não conferem."
            )
        }), 400


    # -----------------------------------------------------
    # GERA HASH
    # -----------------------------------------------------

    senha_hash = generate_password_hash(
        nova_senha
    )


    # -----------------------------------------------------
    # ATUALIZA BANCO
    # -----------------------------------------------------

    db = get_db()


    db.execute(
        """
        UPDATE usuarios
        SET senha = ?
        WHERE id = ?
        """,
        (
            senha_hash,
            usuario_id
        )
    )


    db.commit()


    # -----------------------------------------------------
    # INVALIDA RECUPERAÇÃO
    # -----------------------------------------------------

    session.pop(
        "recuperacao_usuario_id",
        None
    )

    session.pop(
        "recuperacao_codigo_hash",
        None
    )

    session.pop(
        "recuperacao_expira",
        None
    )

    session.pop(
        "recuperacao_verificada",
        None
    )


    return jsonify({
        "sucesso": True,
        "mensagem": (
            "Senha alterada com sucesso."
        )
    })

# =========================================================
# ATIVAR TESTE GRÁTIS (14 DIAS)
# =========================================================

@auth_bp.route("/ativar-teste", methods=["POST"])
def ativar_teste():

    if "usuario_id" not in session:
        return jsonify({
            "sucesso": False,
            "erro": "Faça login para ativar o teste gratuito."
        }), 401

    db = get_db()

    usuario_id = session["usuario_id"]

    hoje = datetime.now()
    fim = hoje + timedelta(days=14)

    db.execute(
        """
        UPDATE usuarios
        SET periodo_teste = ?,
            trial_fim = ?
        WHERE id = ?
        """,
        (
            14,
            fim.isoformat(),
            usuario_id
        )
    )

    db.commit()

    return jsonify({
        "sucesso": True,
        "mensagem": "Teste gratuito ativado!",
        "expira": fim.strftime("%d/%m/%Y")
    })

# =========================================================
# LOGOUT
# =========================================================

@auth_bp.route(
    "/logout"
)
def logout():

    if "usuario_id" in session:

        limpar_remember_token(
            session["usuario_id"]
        )


    session.clear()


    resposta = make_response(
        redirect(
            url_for("inicio")
        )
    )


    resposta.delete_cookie(
        "remember_token"
    )


    return resposta