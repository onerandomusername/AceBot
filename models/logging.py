from __future__ import annotations

import enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from models.base import Base


class CommandType(enum.Enum):
    PREFIX = enum.auto()
    APPLICATION = enum.auto()


class Log(MappedAsDataclass, Base):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    channel_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    command: Mapped[str] = mapped_column(sa.Text(), nullable=False)
    type: Mapped[CommandType] = mapped_column(
        sa.Enum(CommandType, name="command_type"), nullable=False
    )
