from flask import Blueprint, request, redirect, url_for, session, make_response, render_template, jsonify

from models.usuario import (
    criar_usuario,
    validar_login,
    gerar_remember_token,
    limpar_remember_token,
    buscar_usuario_por_cnpj_ou_email
)


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/cadastro", methods=["POST"])
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


@auth_bp.route("/login", methods=["POST"])
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

        token = gerar_remember_token(usuario["id"])

        resposta = make_response(
            redirect(
                url_for("dashboard.dashboard")
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


@auth_bp.route("/recuperar-senha", methods=["POST"])
def recuperar_senha():

    from models.usuario import buscar_usuario_por_cnpj_ou_email
    import random

    identificacao = request.form["identificacao"]

    usuario = buscar_usuario_por_cnpj_ou_email(
        identificacao
    )

    if usuario is None:
        return "Usuário não encontrado"

    codigo = random.randint(100000, 999999)

    telefone = usuario[3]

    print("USUARIO:", usuario)
    print("TELEFONE:", usuario[3])

    mensagem = (
        f"Seu código de recuperação do CotaFarma é: {codigo}"
    )

    from urllib.parse import quote

    link = (
        f"https://wa.me/{telefone}"
        f"?text={quote(mensagem)}"
    )

    return redirect(link)

@auth_bp.route("/logout")
def logout():

    if "usuario_id" in session:
        limpar_remember_token(session["usuario_id"])

    session.clear()

    resposta = make_response(
        redirect(url_for("inicio"))
    )

    resposta.delete_cookie("remember_token")

    return resposta