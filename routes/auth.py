from flask import Blueprint, render_template, request


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        cnpj = request.form.get("cnpj")
        senha = request.form.get("senha")

        print("Login:", cnpj)

        # depois vamos ligar ao Turso

    return render_template("login.html")