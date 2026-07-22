from flask import Blueprint, render_template, request, redirect, url_for, session

from database.connection import get_db

cotacao_bp = Blueprint("cotacao", __name__)


@cotacao_bp.route("/cotacoes")
def cotacoes():
    return render_template("cotacoes.html")


@cotacao_bp.route("/cotacoes/criar", methods=["POST"])
def criar_cotacao():

    db = get_db()

    # Use a mesma chave que foi salva no login
    cnpj = session.get("usuario_cnpj")

    nome = request.form.get("nome_cotacao")
    medicamento = request.form.get("medicamento")
    laboratorio = request.form.get("laboratorio")
    quantidade = request.form.get("quantidade")

    cursor = db.execute(
        """
        INSERT INTO cotacoes (
            cnpj_usuario,
            nome,
            status
        )
        VALUES (?, ?, 'RASCUNHO')
        """,
        (cnpj, nome)
    )

    cotacao_id = cursor.lastrowid

    db.execute(
        """
        INSERT INTO cotacao_itens (
            cotacao_id,
            medicamento,
            laboratorio,
            quantidade
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            cotacao_id,
            medicamento,
            laboratorio,
            quantidade
        )
    )

    db.commit()

    return redirect(url_for("dashboard.dashboard"))