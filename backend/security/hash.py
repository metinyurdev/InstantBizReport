from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Şifreyi hash'ler.
    
    Args:
        password (str): Hash'lenecek düz metin şifre.
    
    Returns:
        str: Hash'lenmiş şifre.
    """
    return pwd_context.hash(password)