from dataclasses import dataclass

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import EncryptedMessage


@dataclass(slots=True)
class EncryptionRepository:
    session: AsyncSession

    async def get_message_by_secret_key(self, secret_key: str) -> EncryptedMessage:
        query = select(EncryptedMessage).filter(
            EncryptedMessage.secret_key == secret_key,
            EncryptedMessage.is_removed.is_(False),
        )
        return await self.session.scalar(query)

    async def save_encrypted_message(self, text: bytes, secret_key: str) -> None:
        message = EncryptedMessage(text=text, secret_key=secret_key)
        self.session.add(message)
        await self.session.commit()

    async def remove_message(self, secret_key: str) -> None:
        query = (
            update(EncryptedMessage)
            .filter(EncryptedMessage.secret_key == secret_key)
            .values(is_removed=True)
        )
        await self.session.execute(query)
        await self.session.commit()
