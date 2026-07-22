from database.connection import get_db
from werkzeug.security import generate_password_hash

db = get_db()

cnpj = "48781467000142"
nova_senha = "0000"

hash_senha = generate_password_hash(nova_senha)

db.execute(
    "UPDATE usuarios SET senha = ? WHERE cnpj = ?",
    (hash_senha, cnpj)
)

db.commit()

print("Senha atualizada com sucesso!")