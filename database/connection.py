import os
import libsql
from dotenv import load_dotenv

load_dotenv()


def get_db():

    url = os.getenv("TURSO_DATABASE_URL")
    token = os.getenv("TURSO_AUTH_TOKEN")

    db = libsql.connect(
        "local.db",
        sync_url=url,
        auth_token=token
    )

    try:
        db.sync()
    except Exception as e:
        print("Aviso: não foi possível sincronizar com o Turso.")
        print(e)

    return db