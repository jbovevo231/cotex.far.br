from database.connection import get_db


def buscar_comparativo(cotacao_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            medicamento,
            representante,
            distribuidora,
            status,
            preco,
            preco_oferta,
            quantidade_oferta
        FROM respostas_cotacao
        WHERE cotacao_id = ?
        ORDER BY medicamento
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

        comparativo[medicamento]["representantes"].append({
            "representante": item[1],
            "laboratorio": item[2],
            "preco": item[4],
            "preco_oferta": item[5],
            "quantidade": item[6],
            "oferta": status == "OFERTA",
            "menor_preco": False
        })

        # Marca apenas UM representante com o menor preço
    for med in comparativo.values():

        menor_indice = None
        menor_valor = None

    for i, r in enumerate(med["representantes"]):

        # Usa o preço da oferta quando houver
        preco = r["preco_oferta"] if r["oferta"] else r["preco"]

        if preco in (None, ""):
            continue

        try:
            valor = float(str(preco).replace(",", "."))

            # Usa apenas "<" para que, em caso de empate,
            # permaneça o primeiro representante.
            if menor_valor is None or valor < menor_valor:
                menor_valor = valor
                menor_indice = i

        except (ValueError, TypeError):
            continue

    if menor_indice is not None:
        med["representantes"][menor_indice]["menor_preco"] = True

    print(comparativo)

    return list(comparativo.values())

def buscar_resultado(cotacao_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            medicamento,
            quantidade_oferta,
            representante,
            distribuidora,
            preco,
            preco_oferta,
            status
        FROM respostas_cotacao
        WHERE cotacao_id = ?
        ORDER BY medicamento
    """, (cotacao_id,))

    dados = cursor.fetchall()

    db.close()

    return dados