from pydantic import BaseModel, Field


class SecretKey(BaseModel):
    secret_key: str = Field(..., title="Key to receive the message")

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    text: str = Field(..., title="Message text")

    class Config:
        orm_mode = True
