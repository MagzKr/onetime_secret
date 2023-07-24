from cryptography.fernet import InvalidToken
from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field
from starlette import status

from app.api.deps import get_encryption_service
from app.api.schemas.requests import MessageRequest, PasswordRequest
from app.api.schemas.responses import MessageResponse, SecretKey
from app.core.services import EncryptionService

router = APIRouter()


@router.post("/generate", response_model=SecretKey, name="messages:generate")
async def create_secret_message(
    message: MessageRequest,
    encryption_service: EncryptionService = Depends(get_encryption_service),
) -> SecretKey:
    """Generate secret message"""
    encrypted_message = encryption_service.encrypt_message_by_password(
        message=message.text.encode(), password=message.password
    )
    secret_key = await encryption_service.create_unique_secret_key()
    await encryption_service.save_encrypted_message(
        text=encrypted_message, secret_key=secret_key
    )

    return SecretKey(secret_key=secret_key)


@router.post(
    "/secrets/{secret_key}", response_model=MessageResponse, name="messages:read"
)
async def read_current_user(
    password: PasswordRequest,
    secret_key: str = Field(..., max_length=128),
    encryption_service: EncryptionService = Depends(get_encryption_service),
) -> MessageResponse:
    """Get message by secret_key"""
    message = await encryption_service.get_message_by_secret_key(secret_key=secret_key)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message with that secret key not found",
        )
    try:
        decrypted_text = encryption_service.decrypt_message_by_password(
            message.text, password.password
        )
    except InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Password is invalid"
        )
    await encryption_service.remove_message(secret_key)

    return MessageResponse(text=decrypted_text)
