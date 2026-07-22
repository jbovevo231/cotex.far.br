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

        preco = item[4] if status == "TENHO" else item[5]

        comparativo[medicamento]["representantes"].append({
            "representante": item[1],
            "laboratorio": item[2],
            "preco": preco,
            "quantidade": item[6],
            "oferta": status == "OFERTA",
            "menor_preco": False
        })

    # Marca o menor preço de cada medicamento
    for med in comparativo.values():

        precos = []

        for r in med["representantes"]:

            if r["preco"] not in (None, ""):
                try:
                    valor = float(str(r["preco"]).replace(",", "."))
                    precos.append(valor)
                except:
                    pass

        if not precos:
            continue

        menor = min(precos)

        for r in med["representantes"]:

            if r["preco"] not in (None, ""):
                try:
                    valor = float(str(r["preco"]).replace(",", "."))

                    if valor == menor:
                        r["menor_preco"] = True

                except:
                    pass

    return list(comparativo.values())