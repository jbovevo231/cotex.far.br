from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect,
    url_for,
    jsonify
)

from database.connection import get_db

from services.dashboard_service import (
    carregar_indicadores,
    carregar_ultimas_cotacoes
)

print(">>>>>>>> DASHBOARD.PY FOI CARREGADO <<<<<<<<")
print(__file__)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
def dashboard():

    cnpj = session.get("usuario_cnpj")


    indicadores = carregar_indicadores(cnpj)


    print("===================================")
    print(indicadores)
    print("===================================")


    ultimas_cotacoes = carregar_ultimas_cotacoes(cnpj)



    return render_template(
        "dashboard.html",
        indicadores=indicadores,
        ultimas_cotacoes=ultimas_cotacoes
    )

print(">>> ROTA PENDÊNCIAS CARREGADA <<<")

@dashboard_bp.route("/dashboard/pendencias")
def dashboard_pendencias():

    if "usuario_cnpj" not in session:
        return jsonify([])

    cnpj = session["usuario_cnpj"]

    conn = get_db()

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.medicamento,
                p.laboratorio,
                p.quantidade
            FROM itens_pendentes p
            INNER JOIN cotacoes c
                ON c.id = p.cotacao_origem
            WHERE c.cnpj_usuario = ?
            ORDER BY p.data_registro DESC
        """, (cnpj,))

        pendencias = cursor.fetchall()

        resultado = []

        for item in pendencias:

            resultado.append([
                item[0],
                item[1],
                item[2]
            ])

        return jsonify(resultado)

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify({
            "erro": str(e)
        }), 500

    finally:

        conn.close()

@dashboard_bp.route("/dashboard/historico")
def dashboard_historico():

    from models.cotacao import buscar_historico

    termo = request.args.get("q", "").strip()

    return jsonify(
        buscar_historico(
            session["usuario_cnpj"],
            termo
        )
    )

# ==========================================
# CONFIGURAÇÕES
# ==========================================


@dashboard_bp.route("/configuracoes")
def configuracoes():


    from models.usuario import buscar_usuario_por_id


    usuario = buscar_usuario_por_id(
        session["usuario_id"]
    )


    return render_template(
        "configuracoes.html",
        usuario=usuario
    )








# ==========================================
# ATUALIZAR DADOS
# SOMENTE TELEFONE E EMAIL
# ==========================================


@dashboard_bp.route(
    "/configuracoes/editar",
    methods=["POST"]
)
def atualizar_dados():


    from database.connection import get_db



    telefone = request.form["telefone"]

    email = request.form["email"]



    db = get_db()



    db.execute(
        """
        UPDATE usuarios
        SET telefone=?,
            email=?
        WHERE id=?
        """,
        (
            telefone,
            email,
            session["usuario_id"]
        )
    )


    db.commit()



    session["usuario_email"] = email



    return redirect(
        url_for("dashboard.configuracoes")
    )










# ==========================================
# ALTERAR SENHA
# ==========================================


@dashboard_bp.route(
    "/configuracoes/senha",
    methods=["POST"]
)
def alterar_senha():


    from database.connection import get_db

    from werkzeug.security import (
        check_password_hash,
        generate_password_hash
    )



    senha_atual = request.form["senha_atual"].strip()

    nova_senha = request.form["nova_senha"].strip()

    confirmar = request.form["confirmar_senha"].strip()



    # Confirma se as duas senhas são exatamente iguais
    if nova_senha != confirmar:

        return "A confirmação da senha não confere"







    db = get_db()





    usuario = db.execute(
        """
        SELECT senha
        FROM usuarios
        WHERE id=?
        """,
        (
            session["usuario_id"],
        )
    ).fetchone()







    if usuario is None:

        return "Usuário não encontrado"







    if not check_password_hash(
        usuario[0],
        senha_atual
    ):

        return "Senha atual incorreta"







    nova_hash = generate_password_hash(
        nova_senha
    )







    db.execute(
        """
        UPDATE usuarios
        SET senha=?
        WHERE id=?
        """,
        (
            nova_hash,
            session["usuario_id"]
        )
    )



    db.commit()





    return redirect(
        url_for("dashboard.configuracoes")
    )