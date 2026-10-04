import os
import turso_serverless
from dotenv import load_dotenv

load_dotenv()


def get_db():

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

    db = turso_serverless.connect(
        url,
        auth_token=token
    )

    return db