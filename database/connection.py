import os
import libsql
from dotenv import load_dotenv

load_dotenv()

_db = None


def get_db():

    global _db

    if _db is not None:
        return _db

    url = os.getenv("TURSO_DATABASE_URL")
    token = os.getenv("TURSO_AUTH_TOKEN")

    if not url:
        raise RuntimeError(
            "TURSO_DATABASE_URL não configurada"
        )

    if not token:
        raise RuntimeError(
            "TURSO_AUTH_TOKEN não configurado"
        )

    _db = libsql.connect(
        database=url,
        auth_token=token
    )

    return _db