from models.database import *
from werkzeug.security import check_password_hash, generate_password_hash

def verify_password(senha_plain: str, senha_hash: str) -> bool:
    return check_password_hash(senha_hash, senha_plain)

def hash_password(senha_plain: str) -> str:
    return generate_password_hash(senha_plain)