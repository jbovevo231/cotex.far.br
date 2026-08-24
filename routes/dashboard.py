from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect,
    url_for,
    jsonify
)

from datetime import datetime
import math

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

# Integração Asaas será habilitada depois.

@dashboard_bp.route("/assinar/<plano>", methods=["POST"])
def assinar(plano):
    return {"mensagem": "Integração Asaas em desenvolvimento"}

    valor, ciclo = valores[plano]

    cliente = criar_cliente(
        usuario["nome"],
        usuario["email"],
        usuario["cnpj"],
        usuario["telefone"]
    )

    assinatura = criar_assinatura(
        cliente["id"],
        valor,
        ciclo
    )

    return {"checkout": assinatura["invoiceUrl"]}


# ==========================================
# CALCULAR DIAS RESTANTES DO TESTE
# ==========================================

def calcular_dias_restantes(trial_fim):
    if not trial_fim:
        return 0

    try:
        # Funciona tanto com datetime (Turso) quanto com string ISO
        fim = (
            trial_fim
            if isinstance(trial_fim, datetime)
            else datetime.fromisoformat(str(trial_fim))
        )

        segundos = (fim - datetime.now()).total_seconds()

        if segundos <= 0:
            return 0

        return math.ceil(segundos / 86400)

    except Exception as e:
        print("ERRO AO CALCULAR TRIAL:", trial_fim, type(trial_fim), e)
        return 0


@dashboard_bp.route("/dashboard")
def dashboard():

    # Se não estiver logado, volta para a página inicial
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    cnpj = session.get("usuario_cnpj")

    from models.usuario import buscar_usuario_por_id

    usuario = buscar_usuario_por_id(session["usuario_id"])

    print("===================================")
    print("USUARIO LOGADO:", usuario)
    print("CNPJ:", cnpj)
    print("===================================")

    nome_farmacia = "Farmácia"

    if usuario:
        nome_farmacia = usuario.get("nome", "Farmácia")

    # ==========================================
    # PLANO E DIAS RESTANTES (SIDEBAR)
    # ==========================================

    plano = usuario.get("plano", "teste")
    dias_restantes = calcular_dias_restantes(usuario.get("trial_fim"))

    # ==========================================
    # INDICADORES
    # ==========================================

    indicadores = carregar_indicadores(cnpj)

    # ==========================================
    # MÊS ATUAL
    # ==========================================

    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    mes_atual = meses[datetime.now().month - 1]
    indicadores["mes_atual"] = mes_atual

    # ==========================================
    # ÚLTIMAS COTAÇÕES
    # ==========================================

    ultimas_cotacoes = carregar_ultimas_cotacoes(cnpj)

    return render_template(
        "dashboard.html",
        indicadores=indicadores,
        ultimas_cotacoes=ultimas_cotacoes,
        nome_farmacia=nome_farmacia,
        mes_atual=mes_atual,
        usuario=usuario,
        plano=plano,
        dias_restantes=dias_restantes
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

    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    from models.usuario import buscar_usuario_por_id

    usuario = buscar_usuario_por_id(session["usuario_id"])

    plano = usuario.get("plano", "teste")
    dias_restantes = calcular_dias_restantes(usuario.get("trial_fim"))

    return render_template(
        "configuracoes.html",
        usuario=usuario,
        plano=plano,
        dias_restantes=dias_restantes
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


# ==========================================
# TABELA CMED
# ==========================================

@dashboard_bp.route("/tabela-cmed")
def tabela_cmed():

    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    from models.usuario import buscar_usuario_por_id

    usuario = buscar_usuario_por_id(session["usuario_id"])

    plano = usuario.get("plano", "teste")
    dias_restantes = calcular_dias_restantes(usuario.get("trial_fim"))

    margem = usuario.get("margem_padrao", 25)

    termo = request.args.get("q", "").strip()

    conn = get_db()
    cursor = conn.cursor()

    medicamentos = []

    if termo:

        cursor.execute("""
            SELECT
                principio_ativo,
                apresentacao,
                laboratorio,
                pf,
                pmc
            FROM tabela_cmed
            WHERE LOWER(principio_ativo) LIKE LOWER(?)
               OR LOWER(apresentacao) LIKE LOWER(?)
               OR LOWER(laboratorio) LIKE LOWER(?)
            ORDER BY principio_ativo
            LIMIT 50
        """, (
            f"%{termo}%",
            f"%{termo}%",
            f"%{termo}%"
        ))

        resultados = cursor.fetchall()

        for m in resultados:

            medicamentos.append([
                m[0],          # princípio ativo
                m[1],          # apresentação
                m[2],          # laboratório
                m[3],          # PF (número)
                m[4]           # PMC (número)
            ])

    conn.close()

    return render_template(
        "tabela_cmed.html",
        usuario=usuario,
        plano=plano,
        dias_restantes=dias_restantes,
        medicamentos=medicamentos,
        termo=termo,
        margem=margem
    )