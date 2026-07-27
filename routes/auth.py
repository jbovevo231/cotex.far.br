from flask import Blueprint, request, redirect, url_for, session, make_response

from models.usuario import (
    criar_usuario,
    validar_login,
    gerar_remember_token,
    limpar_remember_token
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
    email = request.form["email"]
    senha = request.form["senha"]
    confirmar = request.form["confirmar"]

    if senha != confirmar:
        return "As senhas não conferem"

    criar_usuario(
        nome,
        cpf,
        cnpj,
        email,
        senha
    )

    return redirect(url_for("inicio"))


@auth_bp.route("/login", methods=["POST"])
def login():

    cnpj = request.form["cnpj"]
    senha = request.form["senha"]

    usuario = validar_login(
        cnpj,
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
            max_age=60 * 60 * 24 * 30,  # 30 dias
            httponly=True,
            secure=True,          # Render utiliza HTTPS
            samesite="Lax"
        )

        return resposta

    return "CNPJ ou senha inválidos"


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