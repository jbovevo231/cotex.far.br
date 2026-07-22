from database.connection import get_db
from werkzeug.security import generate_password_hash


db = get_db()

senha_nova = "0000"

novo_hash = generate_password_hash(senha_nova)

print("NOVO HASH:")
print(novo_hash)


db.execute(
    """
    UPDATE usuarios
    SET senha = ?
    WHERE cnpj = ?
    """,
    (
        novo_hash,
        "48781467000142"
    )
)

db.commit()

print("ATUALIZADO")