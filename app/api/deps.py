from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repositories import EncryptionRepository
from app.core.services import EncryptionService
from app.core.session import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_encryption_repository(
    session: AsyncSession = Depends(get_session),
) -> EncryptionRepository:
    return EncryptionRepository(session=session)


async def get_encryption_service(
    encryption_repository: EncryptionRepository = Depends(get_encryption_repository),
) -> EncryptionService:
    return EncryptionService(repository=encryption_repository)
