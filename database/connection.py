import os
import libsql
from dotenv import load_dotenv

load_dotenv()


def get_db():

    url = os.getenv("TURSO_DATABASE_URL")
    token = os.getenv("TURSO_AUTH_TOKEN")

    print("DB 1 - iniciando conexão")
    print("DB URL configurada:", bool(url))
    print("DB TOKEN configurado:", bool(token))

    db = libsql.connect(
        database=url,
        auth_token=token
    )

    print("DB 2 - conexão criada")

    return db