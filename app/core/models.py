"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""

from sqlalchemy import Boolean, Integer, LargeBinary, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class EncryptedMessage(Base):
    __tablename__ = "encrypted_message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    secret_key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    is_removed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
