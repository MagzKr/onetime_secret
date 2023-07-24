import secrets
from base64 import urlsafe_b64decode as b64d
from base64 import urlsafe_b64encode as b64e
from dataclasses import dataclass

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.core.constants import PBKDF2_ITERATIONS, SECRET_KEY_LENGTH
from app.core.models import EncryptedMessage
from app.core.repositories import EncryptionRepository


@dataclass(slots=True)
class EncryptionService:
    repository: EncryptionRepository

    @staticmethod
    def _get_key_by_password(password: bytes, salt: bytes) -> bytes:
        """Derive a secret key from a given password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
            backend=default_backend(),
        )
        return b64e(kdf.derive(password))

    def encrypt_message_by_password(self, message: bytes, password: str) -> bytes:
        salt = secrets.token_bytes(16)
        key = self._get_key_by_password(password.encode(), salt)
        return b64e(
            b"%b%b"
            % (
                salt,
                b64d(Fernet(key).encrypt(message)),
            )
        )

    def decrypt_message_by_password(
        self, encrypted_message: bytes, password: str
    ) -> str:
        decoded = b64d(encrypted_message)
        salt, token = decoded[:16], b64e(decoded[16:])
        key = self._get_key_by_password(password.encode(), salt)
        return Fernet(key).decrypt(token).decode()

    async def create_unique_secret_key(self) -> str:
        secret_key = secrets.token_urlsafe(SECRET_KEY_LENGTH)
        while await self.repository.get_message_by_secret_key(secret_key=secret_key):
            secret_key = secrets.token_urlsafe(SECRET_KEY_LENGTH)
        return secret_key

    async def save_encrypted_message(self, text: bytes, secret_key: str) -> None:
        await self.repository.save_encrypted_message(text=text, secret_key=secret_key)

    async def get_message_by_secret_key(
        self, secret_key: str
    ) -> EncryptedMessage | None:
        return await self.repository.get_message_by_secret_key(secret_key=secret_key)

    async def remove_message(self, secret_key: str) -> None:
        return await self.repository.remove_message(secret_key=secret_key)
