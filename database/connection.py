import os
import libsql
from dotenv import load_dotenv

load_dotenv()


def get_db():

    url = os.getenv("TURSO_DATABASE_URL")
    token = os.getenv("TURSO_AUTH_TOKEN")

    return libsql.connect(
        "local.db",
        sync_url=url,
        auth_token=token
    )