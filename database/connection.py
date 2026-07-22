import os
import libsql
from dotenv import load_dotenv

load_dotenv()

def get_db():

    url = os.getenv("TURSO_DATABASE_URL")
    token = os.getenv("TURSO_AUTH_TOKEN")

    print("URL:", url)
    print("TOKEN:", "OK" if token else "NÃO ENCONTRADO")

    db = libsql.connect(
        "local.db",
        sync_url=url,
        auth_token=token
    )

    db.sync()

    return db