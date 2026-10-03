from database.connection import get_db


def buscar_comparativo(cotacao_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            rc.medicamento,
            rc.representante,
            rc.distribuidora,
            rc.status,
            rc.preco,
            rc.preco_oferta,
            rc.quantidade_oferta,
            ci.quantidade,
            rc.whatsapp
        FROM respostas_cotacao rc

        INNER JOIN cotacao_itens ci
            ON ci.cotacao_id = rc.cotacao_id
           AND ci.medicamento = rc.medicamento

        WHERE rc.cotacao_id = ?

        ORDER BY rc.medicamento
    """, (cotacao_id,))

    dados = cursor.fetchall()

    db.close()

    comparativo = {}

    for item in dados:

        medicamento = item[0]

        if medicamento not in comparativo:
            comparativo[medicamento] = {
                "nome": medicamento,
                "representantes": []
            }

        status = str(item[3]).strip().upper()

        preco = item[5] if status == "OFERTA" else item[4]

        try:
            if preco is None or float(str(preco).replace(",", ".")) <= 0:
                continue
        except (ValueError, TypeError):
            continue

        # OFERTA usa a quantidade mínima digitada pelo representante.
        # TENHO usa a quantidade solicitada na cotação.
        quantidade = item[6] if status == "OFERTA" else item[7]

        comparativo[medicamento]["representantes"].append({
            "representante": item[1],
            "laboratorio": item[2],
            "preco": item[4],
            "preco_oferta": item[5],
            "preco_final": preco,
            "quantidade": quantidade,
            "whatsapp": item[8],
            "oferta": status == "OFERTA",
            "menor_preco": False
        })

    for med in comparativo.values():

        def valor_preco(rep):

            preco = rep["preco_oferta"] if rep["oferta"] else rep["preco"]

            try:
                return float(str(preco).replace(",", "."))
            except (ValueError, TypeError):
                return float("inf")

        med["representantes"].sort(key=valor_preco)

        if med["representantes"]:
            med["representantes"][0]["menor_preco"] = True

    return list(comparativo.values())


def buscar_resultado(cotacao_id):

    comparativo = buscar_comparativo(cotacao_id)

    representantes = {}

    for medicamento in comparativo:

        vencedor = next(
            (
                rep
                for rep in medicamento["representantes"]
                if rep["menor_preco"]
            ),
            None
        )

        if vencedor is None:
            continue

        nome = vencedor["representante"]

        if nome not in representantes:
            representantes[nome] = {
                "representante": nome,
                "distribuidora": vencedor["laboratorio"],
                "whatsapp": vencedor["whatsapp"],
                "itens": []
            }

        representantes[nome]["itens"].append({
            "medicamento": medicamento["nome"],
            "preco": vencedor["preco"],
            "preco_oferta": vencedor["preco_oferta"],
            "preco_final": vencedor["preco_final"],
            "quantidade": vencedor["quantidade"],
            "oferta": vencedor["oferta"]
        })

    # ============================================================
    # ITENS NÃO COTADOS
    # Só entra aqui se TODOS os representantes responderam NÃO TENHO
    # ============================================================

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            rc.medicamento,
            rc.status
        FROM respostas_cotacao rc
        WHERE rc.cotacao_id = ?
        ORDER BY rc.medicamento
    """, (cotacao_id,))

    respostas = cursor.fetchall()

    db.close()

    # Agrupa as respostas por medicamento
    respostas_por_medicamento = {}

    for medicamento, status in respostas:

        if medicamento not in respostas_por_medicamento:
            respostas_por_medicamento[medicamento] = []

        respostas_por_medicamento[medicamento].append(
            str(status).strip().upper()
        )

    itens_nao_cotados = []

    for medicamento, status_list in respostas_por_medicamento.items():

        # Só entra se TODAS as respostas forem NÃO TENHO
        todos_nao_tem = all(
            status in ("NAO_TENHO", "NÃO TENHO")
            for status in status_list
        )

        if todos_nao_tem:
            itens_nao_cotados.append({
                "medicamento": medicamento,
                "situacao": "NÃO TENHO"
            })

    resultado = list(representantes.values())

    resultado.append({
        "__tipo": "itens_nao_cotados",
        "itens": itens_nao_cotados
    })

    return resultado