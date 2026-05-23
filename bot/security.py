import hashlib
from cryptography.fernet import Fernet

class SecurityService:
    def __init__(self, key: str):
        self.fernet = Fernet(key.encode())

    def hash_text(self, text: str):
        return hashlib.sha256(text.encode()).hexdigest()

    def encrypt(self, text: str):
        return self.fernet.encrypt(text.encode()).decode()

    def decrypt(self, text: str):
        return self.fernet.decrypt(text.encode()).decode()