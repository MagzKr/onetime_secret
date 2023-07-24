from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to be encrypted")
    password: str = Field(..., min_length=1, description="Passwort to decrypt message")


class PasswordRequest(BaseModel):
    password: str = Field(..., min_length=1, description="Password for message")
