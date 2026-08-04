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
            ci.quantidade
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

    # Monta a lista de representantes por medicamento
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

        print(
    "MED:", medicamento,
    "| QTD:", item[6],
    "| TIPO:", type(item[6])
)

        comparativo[medicamento]["representantes"].append({
            "representante": item[1],
            "laboratorio": item[2],
            "preco": item[4],
            "preco_oferta": item[5],
            "quantidade": item[6],
            "oferta": status == "OFERTA",
            "menor_preco": False
        })

    # Ordena os representantes pelo menor preço e marca o vencedor
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

        


        # Ordena os representantes pelo menor preço e marca o vencedor
    for med in comparativo.values():

        def valor_preco(rep):

            preco = rep["preco_oferta"] if rep["oferta"] else rep["preco"]

            try:
                return float(str(preco).replace(",", "."))
            except (ValueError, TypeError):
                return float("inf")

        # Ordena do menor para o maior
        med["representantes"].sort(key=valor_preco)

        # Marca apenas o primeiro como vencedor
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
                "itens": []
            }

        representantes[nome]["itens"].append({
            "medicamento": medicamento["nome"],
            "preco": vencedor["preco"],
            "preco_oferta": vencedor["preco_oferta"],
            "quantidade": vencedor["quantidade"],
            "oferta": vencedor["oferta"]
        })

    return list(representantes.values())

    print(representantes)

def buscar_pedido(cotacao_id, representante):

    resultado = buscar_resultado(cotacao_id)

    for rep in resultado:

        if rep["representante"] == representante:

            return {
                "representante": rep["representante"],
                "distribuidora": rep["distribuidora"],
                "itens": rep["itens"]
            }

    return {
        "representante": representante,
        "distribuidora": "",
        "itens": []
    }