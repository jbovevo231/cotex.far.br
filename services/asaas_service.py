import os
import requests

BASE_URL = os.getenv("ASAAS_BASE_URL", "https://api.asaas.com/v3")
API_KEY = os.getenv("ASAAS_API_KEY")

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "access_token": API_KEY
}


def criar_cliente(nome, email, cpf_cnpj, telefone):
    payload = {
        "name": nome,
        "email": email,
        "cpfCnpj": cpf_cnpj,
        "mobilePhone": telefone
    }

    r = requests.post(
        f"{BASE_URL}/customers",
        json=payload,
        headers=HEADERS
    )

    return r.json()


def criar_assinatura(customer_id, valor, ciclo):

    payload = {
        "customer": customer_id,
        "billingType": "UNDEFINED",
        "value": valor,
        "cycle": ciclo,
        "description": "Assinatura CotaUP Premium"
    }

    r = requests.post(
        f"{BASE_URL}/subscriptions",
        json=payload,
        headers=HEADERS
    )

    return r.json()