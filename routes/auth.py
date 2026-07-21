from flask import Blueprint, request, redirect, url_for, session

from models.usuario import criar_usuario, validar_login


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
        session["usuario_email"] = usuario["email"]
        session["usuario_cnpj"] = usuario["cnpj"]

        return redirect(
            url_for("dashboard.dashboard")
        )


    return "CNPJ ou senha inválidos"