import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "cotex-farma-v2"
    )

    TURSO_DATABASE_URL = os.getenv(
        "TURSO_DATABASE_URL"
    )

    TURSO_AUTH_TOKEN = os.getenv(
        "TURSO_AUTH_TOKEN"
    )