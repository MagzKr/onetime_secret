from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import EncryptedMessage
from app.main import app


async def test_generate_encrypted_message(client: AsyncClient, session: AsyncSession):
    body = {"text": "test", "password": "123"}
    response = await client.post(app.url_path_for("messages:generate"), json=body)
    assert response.status_code == 200

    data = response.json()
    secret_key = data["secret_key"]
    assert secret_key
    result = await session.execute(
        select(EncryptedMessage).where(EncryptedMessage.secret_key == secret_key)
    )
    message = result.scalars().first()
    assert message.text
    assert message.text != body["text"]


async def test_read_decrypted_message(client: AsyncClient, session: AsyncSession):
    body = {"text": "test", "password": "123"}
    response = await client.post(app.url_path_for("messages:generate"), json=body)
    assert response.status_code == 200
    data = response.json()
    secret_key = data["secret_key"]
    assert secret_key

    response = await client.post(
        f"/secrets/{secret_key}", json={"password": body["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == body["text"]
    result = await session.execute(
        select(EncryptedMessage).where(EncryptedMessage.secret_key == secret_key)
    )
    message = result.scalars().first()
    assert message.is_removed is True


async def test_read_decrypted_by_invalid_password(client: AsyncClient):
    body = {"text": "test", "password": "123"}
    response = await client.post(app.url_path_for("messages:generate"), json=body)
    assert response.status_code == 200
    data = response.json()
    secret_key = data["secret_key"]
    assert secret_key

    response = await client.post(f"/secrets/{secret_key}", json={"password": "321"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Password is invalid"}


async def test_read_decrypted_message_404(client: AsyncClient):
    response = await client.post("/secrets/123", json={"password": "321"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Message with that secret key not found"}
